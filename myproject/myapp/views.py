import os
import subprocess
import shutil
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
import asyncio

async def run_game(game_path: str, folder_name: str):
    try:
        terminal_process = await asyncio.create_subprocess_shell(
            "/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        cd_command = f"cd {game_path}"
        terminal_process.stdin.write(cd_command.encode() + b'\n')
        await terminal_process.stdin.drain()

        start_game_command = "./game"
        terminal_process.stdin.write(start_game_command.encode() + b'\n')
        await terminal_process.stdin.drain()

        await asyncio.sleep(5) 

        bd_file_path = f'../Game/bd/result.txt'

        if os.path.exists(bd_file_path):
            return bd_file_path
        else:
            return None

    except Exception as e:
        print(f"Ошибка при запуске терминала или выполнении команды: {e}")
        return None

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # folder_name = form.cleaned_data['folder_name']
            cpp_file = request.FILES['cpp_file']
            folder_name = cpp_file.name.split('.')[0]

            folder_path = os.path.join("../Game/Users", folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            fs = FileSystemStorage(location=folder_path)
            file_name = fs.save(cpp_file.name, cpp_file)
            file_path = os.path.join(folder_path, file_name)

            # game_cpp_path = os.path.join("../Game/src", "teamname.txt")
            # with open(game_cpp_path, 'w') as game_file:
            #     game_file.write(f"{folder_name}")

            try:
                dylib_name = file_name.replace('.cpp', '.dylib')
                dylib_path = os.path.join(folder_path, dylib_name)
                compile_command = [
                    "g++",
                    "-shared",
                    "-o", dylib_path,
                    file_path,
                    "-std=c++20"
                ]
                subprocess.run(compile_command, check=True)
                
                game_path = os.path.join("../Game/src", "game.cpp")
                game_executable_path = os.path.join("../Game/src", "game")
                compile_game_command = [
                    "g++",
                    "-o", game_executable_path,
                    game_path,
                    "-ldl",
                    "-std=c++20"
                ]
                subprocess.run(compile_game_command, check=True)

                result_file_path = asyncio.run(run_game("../Game/src", folder_name))
                if result_file_path:
                    return redirect('show_results')
                else:
                    return HttpResponse("Файл результатов не найден")

            except subprocess.CalledProcessError as e:
                return HttpResponse(f'Ошибка компиляции файла "{file_name}": {e}')

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def show_results(request):
    result_file_path = f'../Game/bd/result.txt'
    if os.path.exists(result_file_path):
        with open(result_file_path, 'r') as file:
            lines = file.readlines()
        
        data = {}
        for i in range(0, len(lines), 6):
            player1_name = lines[i].strip().split(': ')[0].split(' ')[1]
            player2_name = lines[i+1].strip().split(': ')[0].split(' ')[1]
            player1_wins = int(lines[i].strip().split(': ')[1])
            player2_wins = int(lines[i+1].strip().split(': ')[1])
            draws = int(lines[i+2].strip().split(': ')[1])
            player1_point = int(lines[i+3].strip().split(': ')[1])
            player2_point = int(lines[i+4].strip().split(': ')[1])

            if player1_name not in data:
                data[player1_name] = [0, 0, 0, 0.0]
            if player2_name not in data:
                data[player2_name] = [0, 0, 0, 0.0]

            data[player1_name][0] += player1_wins
            data[player1_name][1] += player2_wins
            data[player1_name][2] += draws
            data[player1_name][3] += player1_point

            data[player2_name][0] += player2_wins
            data[player2_name][1] += player1_wins
            data[player2_name][2] += draws
            data[player2_name][3] += player2_point
        
        table_data = []
        for player, stats in data.items():
            total_games = stats[0] + stats[1] + stats[2]
            avg_percent = stats[3] / (10 * total_games) * 100 if total_games > 0 else 0
            table_data.append([player, stats[0], stats[1], stats[2], avg_percent])
        
        table_data.sort(key=lambda x: x[4], reverse=True)
        
        columns = ['Team_name', 'Wins', 'Loses', 'Draws', 'Percent of points']
        df = pd.DataFrame(table_data, columns=columns)
        table_html = df.to_html(classes='data', header="true", index=False)

        return render(request, 'results.html', {'table': table_html})
    else:
        return HttpResponse("Файл результатов не найден")
