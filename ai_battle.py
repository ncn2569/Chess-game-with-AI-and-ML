#!/usr/bin/env python3
"""
AI Battle Arena - Đấu trường cho các AI agents
"""

import sys
import os

# Thêm thư mục dự án vào path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from src.ai_battle import RandomAgent, MinimaxAgent, MLAgent, run_tournament
from src import config

def display_menu():
    """Hiển thị menu chọn AI agents"""
    print("\nAI BATTLE ARENA")
    print("=" * 40)
    print("Chọn 2 AI agents để đấu:")
    print("1. Random AI - Chọn nước đi ngẫu nhiên")
    print("2. Minimax AI (Depth 1) - Nhanh")
    print("3. Minimax AI (Depth 2) - Trung bình")  
    print("4. Minimax AI (Depth 3) - Chậm nhưng mạnh")
    print("5. ML AI - Machine Learning (chưa có code)")
    print("0. Thoát")
    print("=" * 40)

def create_agent(choice: int):
    """Tạo AI agent dựa trên lựa chọn"""
    if choice == 1:
        return RandomAgent()
    elif choice == 2:
        return MinimaxAgent(depth=1)
    elif choice == 3:
        return MinimaxAgent(depth=2)
    elif choice == 4:
        return MinimaxAgent(depth=3)
    elif choice == 5:
        return MLAgent()
    else:
        return None

def get_user_input():
    """Lấy input từ người dùng"""
    try:
        while True:
            display_menu()
            
            # Chọn Agent 1
            choice1 = int(input("\nChọn Agent 1: "))
            if choice1 == 0:
                return None, None, 0
            
            agent1 = create_agent(choice1)
            if agent1 is None:
                print("❌ Lựa chọn không hợp lệ!")
                continue
            
            # Chọn Agent 2
            choice2 = int(input(f"Chọn Agent 2 (đấu với {agent1.name}): "))
            if choice2 == 0:
                return None, None, 0
                
            agent2 = create_agent(choice2)
            if agent2 is None:
                print("Lựa chọn không hợp lệ!")
                continue
            
            # Số ván đấu
            num_games = int(input("\n⚔️  Số ván đấu (nên chạy nhiều nhiều vô để test): "))
            if num_games <= 0:
                print("❌ Số ván đấu phải > 0!")
                continue
            
            return agent1, agent2, num_games
            
    except ValueError:
        print("❌ Vui lòng nhập số!")
        return get_user_input()
    except KeyboardInterrupt:
        print("\nTạm biệt!")
        return None, None, 0

# def run_predefined_battles():
#     """Chạy các trận đấu định sẵn để demo"""
#     print("\nCHẠY DEMO BATTLES")
#     print("=" * 50)
    
#     # Battle 1: Random vs Minimax Depth 1
#     print("\nBATTLE 1: Random vs Minimax (Depth 1)")
#     agent1 = RandomAgent()
#     agent2 = MinimaxAgent(depth=1)
#     run_tournament(agent1, agent2, num_games=5)
    
#     # Battle 2: Minimax Depth 1 vs Depth 2
#     print("\nBATTLE 2: Minimax Depth 1 vs Depth 2")
#     agent1 = MinimaxAgent(depth=1)
#     agent2 = MinimaxAgent(depth=2)
#     run_tournament(agent1, agent2, num_games=5)

def main():
    """Main function"""
    print("CHESS AI BATTLE SYSTEM")
    print("Hệ thống đấu AI cho Chess Game")
    print("Sử dụng để so sánh hiệu suất các AI agents")
    
    while True:
        print("\nMENU CHÍNH:")
        print("1. Tự chọn 2 AI để đấu")
        print("2. Battle Random vs Minimax (khuyến nghị)")
        print("0. Thoát")
        
        try:
            choice = int(input("\n👉 Chọn: "))
            
            if choice == 0:
                print("👋 Tạm biệt!")
                break
            elif choice == 1:
                agent1, agent2, num_games = get_user_input()
                if agent1 and agent2:
                    run_tournament(agent1, agent2, num_games)
            elif choice == 2:
                print("\n BATTLE: Random vs Minimax")
                agent1 = RandomAgent()
                agent2 = MinimaxAgent(depth=config.BATTLE_SEARCH_DEPTH)
                
                num_games = int(input("Số ván đấu (khuyến nghị 10): ") or "10")
                run_tournament(agent1, agent2, num_games)
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break

if __name__ == "__main__":
    main()