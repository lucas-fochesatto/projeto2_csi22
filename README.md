# Viagem Espacial

Jogo 2D de esquiva espacial desenvolvido em Python com pygame. Controle uma nave e desvie de obstáculos (cometas, planetas, satélites e outras ameaças) enquanto acumula pontos.

## Pré-requisitos

- Python 3.8 ou superior
- pip
- **macOS:** SDL2 (necessário para compilar o pygame)

```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
```

## Instalação

**1. Clone o repositório**

```bash
git clone <url-do-repositorio>
cd projeto2
```

**2. (Opcional) Crie e ative um ambiente virtual**

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

## Como rodar

```bash
python main.py
```

## Controles

| Tecla | Ação |
|-------|------|
| `←` Seta esquerda | Mover nave para a esquerda |
| `→` Seta direita | Mover nave para a direita |

## Regras

- Desvie dos obstáculos que descem pela tela para acumular pontos
- Cada obstáculo desviado vale **10 pontos**
- Bater nas laterais exibe uma mensagem de colisão e reinicia a partida
- Colidir com um obstáculo encerra o jogo (**Game Over**)
