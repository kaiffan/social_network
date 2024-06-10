from http.server import BaseHTTPRequestHandler, HTTPServer
import os


# Класс обработчика запросов
class ImageUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers['Content-Type']

        if 'image' in content_type:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            with open('uploads/uploaded_image.jpg', 'wb') as f:
                f.write(post_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Image uploaded successfully.')
        else:
            # Если тип содержимого не является изображением, возвращаем ошибку
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid content type.')


def run(server_class=HTTPServer, handler_class=ImageUploadHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server started on port {port}')
    httpd.serve_forever()


# Запуск сервера
if __name__ == '__main__':
    run()
