#!/usr/bin/env python3
"""
Скрипт для генерации секретного ключа для JWT токенов
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("=" * 60)
    print("Сгенерированный SECRET_KEY:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nСкопируйте этот ключ и добавьте в файл backend/.env")
    print("как значение переменной SECRET_KEY")
    print("=" * 60)
