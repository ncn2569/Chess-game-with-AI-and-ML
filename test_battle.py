#!/usr/bin/env python3
"""
Quick test cho AI Battle System
"""

import sys
import os

# Thêm thư mục dự án vào path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_ai_agents():
    """Test các AI agents cơ bản"""
    try:
        from src.ai_battle import RandomAgent, MinimaxAgent, play_game
        from src import config
        
        print("🧪 Test AI Agents:")
        
        # Test Random Agent
        random_agent = RandomAgent()
        print(f"✅ {random_agent.name}: {random_agent.description}")
        
        # Test Minimax Agent
        minimax_agent = MinimaxAgent(depth=1)
        print(f"✅ {minimax_agent.name}: {minimax_agent.description}")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test agents: {e}")
        return False

def test_single_game():
    """Test một game đơn lẻ"""
    try:
        from src.ai_battle import RandomAgent, MinimaxAgent, play_game
        
        print("\n🎮 Test Single Game:")
        
        agent1 = RandomAgent()
        agent2 = MinimaxAgent(depth=1)
        
        print(f"🤖 {agent1.name} vs {agent2.name}")
        
        result = play_game(agent1, agent2, silent=False, max_moves=50)
        
        print(f"🏁 Kết quả: {result.winner} ({result.reason})")
        print(f"📊 Số nước: {result.moves_count}")
        print(f"⏱️  Thời gian: {result.total_time:.2f}s")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test game: {e}")
        return False

def test_mini_tournament():
    """Test tournament nhỏ"""
    try:
        from src.ai_battle import RandomAgent, MinimaxAgent, run_tournament
        
        print("\n🏆 Test Mini Tournament:")
        
        agent1 = RandomAgent()
        agent2 = MinimaxAgent(depth=1)
        
        results = run_tournament(agent1, agent2, num_games=3)
        
        print("✅ Tournament hoàn thành!")
        print(f"📊 Win rate 1: {results['win_rate1']:.1f}%")
        print(f"📊 Win rate 2: {results['win_rate2']:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test tournament: {e}")
        return False

def test_battle_config():
    """Test cấu hình battle"""
    try:
        from src import config
        
        print("\n⚙️  Test Battle Config:")
        print(f"✅ Battle depth: {config.BATTLE_SEARCH_DEPTH}")
        print(f"✅ Time limit: {config.BATTLE_TIME_LIMIT}s")
        print(f"✅ Max moves: {config.MAX_MOVES_PER_GAME}")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi test config: {e}")
        return False

def main():
    print("🧪 Quick Test - AI Battle System")
    print("=" * 50)
    
    os.chdir(project_dir)
    
    tests = [
        ("AI Agents", test_ai_agents),
        ("Battle Config", test_battle_config),
        ("Single Game", test_single_game),
        ("Mini Tournament", test_mini_tournament)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("📊 Kết quả test:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Tổng kết: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 Battle System sẵn sàng!")
        print("\n📋 Có thể chạy:")
        print("  python ai_battle.py")
    else:
        print("⚠️  Battle System cần kiểm tra thêm.")

if __name__ == "__main__":
    main()