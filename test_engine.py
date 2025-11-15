#!/usr/bin/env python3
"""
Test script cho Minimax Engine
"""

import sys
import os
import time

# Thêm thư mục dự án vào path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_engine_basic():
    """Test cơ bản của engine"""
    try:
        import chess
        from src import engine, config
        
        print("🧠 Test Minimax Engine:")
        
        # Tạo bàn cờ test
        board = chess.Board()
        
        # Test với depth nhỏ
        print("\n📋 Test depth 1:")
        move = engine.find_best_move(board, config.STANDARD_WEIGHTS, 1)
        print(f"✅ Nước đi tìm được: {move.uci() if move else 'None'}")
        
        print("\n📋 Test depth 2:")
        move = engine.find_best_move(board, config.STANDARD_WEIGHTS, 2)
        print(f"✅ Nước đi tìm được: {move.uci() if move else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test engine: {e}")
        return False

def test_evaluation():
    """Test hàm đánh giá"""
    try:
        import chess
        from src import evaluation, config
        
        print("\n🎯 Test Evaluation Function:")
        
        # Test với bàn cờ ban đầu (nên bằng 0)
        board = chess.Board()
        score = evaluation.evaluate_board(board, config.STANDARD_WEIGHTS)
        print(f"✅ Bàn cờ ban đầu: {score} (nên gần 0)")
        
        # Test với bàn cờ có lợi thế cho trắng
        board = chess.Board("rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4")
        score = evaluation.evaluate_board(board, config.STANDARD_WEIGHTS)
        print(f"✅ Thế cờ cân bằng: {score}")
        
        # Test với trắng thiếu quân
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1")
        score = evaluation.evaluate_board(board, config.STANDARD_WEIGHTS)
        print(f"✅ Trắng thiếu 1 mã: {score} (nên âm)")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test evaluation: {e}")
        return False

def test_performance():
    """Test hiệu suất của engine"""
    try:
        import chess
        from src import engine, config
        
        print("\n⚡ Test Performance:")
        
        board = chess.Board()
        depths = [1, 2, 3]
        
        for depth in depths:
            start_time = time.time()
            move = engine.find_best_move(board, config.STANDARD_WEIGHTS, depth)
            end_time = time.time()
            
            elapsed = end_time - start_time
            print(f"✅ Depth {depth}: {elapsed:.3f}s - {move.uci() if move else 'None'}")
            
            if elapsed > 10:  # Nếu quá 10 giây thì warning
                print(f"⚠️  Depth {depth} chậm ({elapsed:.2f}s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test performance: {e}")
        return False

def test_tactical_positions():
    """Test với các thế cờ chiến thuật"""
    try:
        import chess
        from src import engine, config
        
        print("\n🎯 Test Tactical Positions:")
        
        # Test 1: Có thể ăn quân miễn phí
        print("\n📍 Test 1 - Ăn quân miễn phí:")
        board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2")
        board.push_san("Nf3")  # Trắng ra mã
        board.push_san("Nc6")  # Đen ra mã
        board.push_san("Bc4")  # Trắng ra tượng tấn công f7
        # Giờ f7 bị tấn công, AI nên phòng thủ
        
        move = engine.find_best_move(board, config.STANDARD_WEIGHTS, 2)
        print(f"✅ AI chọn: {move.uci() if move else 'None'}")
        
        # Test 2: Tránh bị ăn quân
        print("\n📍 Test 2 - Tránh bị ăn:")
        board = chess.Board("rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 4 4")
        # Mã đen ở f6 có thể bị ăn bởi tốt e4-e5
        
        move = engine.find_best_move(board, config.STANDARD_WEIGHTS, 2)
        print(f"✅ AI chọn: {move.uci() if move else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test tactical: {e}")
        return False

def test_weights():
    """Test với trọng số khác nhau"""
    try:
        import chess
        from src import engine, config
        
        print("\n⚖️  Test Different Weights:")
        
        board = chess.Board()
        
        # Trọng số gốc
        print("\n📊 Trọng số chuẩn:")
        move1 = engine.find_best_move(board, config.STANDARD_WEIGHTS, 2)
        print(f"✅ Nước đi: {move1.uci() if move1 else 'None'}")
        
        # Trọng số ưu tiên hậu
        queen_focused = config.STANDARD_WEIGHTS.copy()
        queen_focused["queen"] = 200
        print("\n👑 Trọng số ưu tiên hậu:")
        print(f"Queen weight: {queen_focused['queen']}")
        move2 = engine.find_best_move(board, queen_focused, 2)
        print(f"✅ Nước đi: {move2.uci() if move2 else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test weights: {e}")
        return False

def main():
    print("🧪 Test Minimax Engine - Chi tiết")
    print("=" * 60)
    
    os.chdir(project_dir)
    
    # Chạy các test
    tests = [
        ("Engine Basic", test_engine_basic),
        ("Evaluation Function", test_evaluation),
        ("Performance", test_performance),
        ("Tactical Positions", test_tactical_positions),
        ("Different Weights", test_weights)
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
    print("\n" + "=" * 60)
    print("📊 Kết quả test:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Tổng kết: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 Engine hoạt động tốt!")
        print("\n📋 Có thể chạy game:")
        print("  python play_game.py")
    else:
        print("⚠️  Engine cần kiểm tra thêm.")

if __name__ == "__main__":
    main()