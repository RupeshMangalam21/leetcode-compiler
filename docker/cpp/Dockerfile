FROM gcc:latest

WORKDIR /app

COPY script.cpp .

RUN g++ script.cpp -o script

CMD ["./script"]
