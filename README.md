# Isometric Garden Simulator

An interactive 2D isometric garden simulation built with Python and Pygame as a Computer Graphics course project. Plant seeds, water them, and watch your garden grow through a day-night cycle with rain, bees, and butterflies.

## Features

- **Isometric tile grid:** a 10x10 garden drawn with isometric projection.
- **Plant growth:** plant crops, flowers, or fruit. Seeds grow into plants once they are watered.
- **Day-night cycle:** the sky colour blends smoothly between day and night, and the on-screen clock shows the day, time, and season.
- **Random rain:** rain falls at random and automatically waters all seeds.
- **Bees:** wander randomly around the scene.
- **Butterflies:** flutter with animated wings, and in the full version they fly to grown plants and land on them.
- **Save and load:** store your garden to a JSON file and restore it later.
- **Simple interface:** buttons to choose the plant type.

## Controls

| Input                            | Action |

|Left click on an empty tile      |Plant a seed of the selected type |
|Right click on a seed            |Water it |
|Bottom buttons(Crop/Flower/Fruit)|Select the plant type |
| `S`                             |Save garden to `garden_save.json`|
| `L`                             | Load the saved garden |

A watered seed grows into a plant after about 5 seconds.

## Computer Graphics Concepts Used

- Isometric projection: converting grid coordinates to screen coordinates (`iso_coords`)
- Polygon rendering for tiles and butterfly wings
- Colour interpolation for the day-night sky
- Particle-style effects for rain
- Frame-based animation using sine functions (wing flapping, butterfly flight)
- Simple agent movement (random walk for bees, target seeking for butterflies)
- A fixed-rate game loop at 60 FPS

## Tech Stack

- Python 3
- Pygame

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/isometric-garden.git
   cd isometric-garden

2. Install the dependency:
  
   pip install -r requirements.txt
   
3. Start the simulation:
   
   python main.py
   

## Project Structure

```
isometric-garden/
├── main.py            # full simulation (butterflies land on grown plants)
├── requirements.txt   # Python dependencies
├── README.md
└──.gitignore


## Author

Samridhi Dahal, B.E. Computer Engineering, Tribhuvan University
Computer Graphics course project