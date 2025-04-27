# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        try:
            file_path = (
                    Path(__file__).parent.parent
                    / "bootstrap-5.3.5-dist"
                    / "contacts.html"
            )
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
            self.send_response(200) # Отправка кода ответа
            self.send_header("Content-type", "text/html; charset=utf-8") # Отправка типа данных, который будет передаваться
            self.end_headers() # Завершение формирования заголовков ответа
            self.wfile.write(bytes(data, "utf-8"))

        except FileNotFoundError:
            self.send_error(404, "File Not Found")

        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

if __name__ == "__main__":
    # найдем свободный порт
    # import socket
    #
    #
    # def find_free_port():
    #     with socket.socket() as s:
    #         s.bind(('', 0))
    #         return s.getsockname()[1]
    #
    #
    # serverPort = find_free_port()

    webServer = None
    try:
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print(f"Сервер запущен: http://{hostName}:{serverPort}")
        webServer.serve_forever()
    except OSError as e:
        print(f"Ошибка: Порт {serverPort} занят. Используйте другой порт.")
    except KeyboardInterrupt:
        print("\nСервер получает сигнал остановки...")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        if webServer:
            webServer.server_close()
            print("Сервер корректно остановлен.")
