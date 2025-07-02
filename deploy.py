"""
Script para facilitar el deployment del proyecto
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Ejecutar comando con descripción"""
    print(f"\n🚀 {description}")
    print(f"Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Éxito!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Error!")
        print(e.stderr)
        return False

def main():
    print("🌟 DEPLOYMENT ASSISTANT - Flappy Bird AI")
    print("="*50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: No se encuentra main.py. Ejecuta este script desde el directorio del proyecto.")
        return
    
    print("\n📋 CHECKLIST PRE-DEPLOYMENT:")
    print("1. ✅ Proyecto inicializado con Git")
    print("2. ✅ Archivos necesarios creados")
    print("3. ✅ Dependencias listadas en requirements.txt")
    
    # Verificar status de Git
    if run_command("git status --porcelain", "Verificando estado de Git"):
        print("📝 Hay cambios pendientes. Creando commit...")
        
        # Add y commit cambios
        run_command("git add .", "Agregando archivos al staging")
        
        commit_message = input("\n💬 Mensaje del commit (Enter para usar mensaje por defecto): ")
        if not commit_message:
            commit_message = "Update project files"
        
        run_command(f'git commit -m "{commit_message}"', "Creando commit")
    
    print("\n🌐 OPCIONES DE DEPLOYMENT:")
    print("1. GitHub Pages (Recomendado para demos estáticos)")
    print("2. Heroku (Para aplicaciones web)")
    print("3. Replit (Fácil y rápido)")
    print("4. Solo crear repositorio en GitHub")
    
    choice = input("\nSelecciona una opción (1-4): ")
    
    if choice == "4" or choice == "":
        print("\n📚 INSTRUCCIONES PARA GITHUB:")
        print("1. Ve a https://github.com/new")
        print("2. Nombre del repositorio: flappi-bird_machine-learning")
        print("3. Descripción: AI learns to play Flappy Bird using NEAT algorithm")
        print("4. Hazlo público")
        print("5. NO agregues README, .gitignore, o licencia (ya los tienes)")
        print("6. Crea el repositorio")
        print("\n7. Luego ejecuta estos comandos:")
        print("   git remote add origin https://github.com/TU-USUARIO/flappi-bird_machine-learning.git")
        print("   git branch -M main")
        print("   git push -u origin main")
    
    elif choice == "1":
        print("\n📄 DEPLOYMENT PARA GITHUB PAGES:")
        print("1. Primero sube el código a GitHub (opción 4)")
        print("2. Ve a Settings > Pages en tu repositorio")
        print("3. Selecciona 'Deploy from a branch'")
        print("4. Elige 'main' branch")
        print("5. Tu demo estará en: https://tu-usuario.github.io/flappi-bird_machine-learning")
        
        print("\n⚠️  NOTA: GitHub Pages no ejecuta Python directamente.")
        print("Necesitarás convertir el proyecto a JavaScript o usar un servicio como Pyodide.")
    
    elif choice == "2":
        print("\n☁️  DEPLOYMENT PARA HEROKU:")
        print("1. Instala Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
        print("2. Ejecuta: heroku login")
        print("3. Ejecuta: heroku create flappy-bird-ai-demo")
        print("4. Ejecuta: git push heroku main")
        print("\n⚠️  NOTA: Heroku tiene limitaciones para juegos con Pygame.")
    
    elif choice == "3":
        print("\n🔧 DEPLOYMENT PARA REPLIT:")
        print("1. Ve a https://replit.com")
        print("2. Crea una cuenta si no tienes")
        print("3. Haz clic en 'Import from GitHub'")
        print("4. Pega la URL de tu repositorio")
        print("5. Replit detectará automáticamente que es Python")
        print("6. Ejecuta el proyecto y compártelo")
    
    print("\n✨ DEMO LOCAL:")
    demo_choice = input("¿Quieres ejecutar el demo local primero? (y/n): ")
    if demo_choice.lower() == 'y':
        print("\n🎮 Ejecutando demo...")
        run_command("python web_demo.py", "Iniciando demo local")
    
    print("\n🎉 ¡Deployment preparado!")
    print("📧 No olvides actualizar el README con la URL de tu demo cuando esté listo.")

if __name__ == "__main__":
    main()
