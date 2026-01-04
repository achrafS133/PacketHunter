from packethunter.fusion import fusion_engine
import time

def test_engine():
    print("Testing Fusion Engine...")
    start = time.time()
    results = fusion_engine()
    elapsed = time.time() - start
    print(f"Results: {results}")
    print(f"Time: {elapsed:.2f}s")
    assert results['total'] > 0
    assert results['ddos'] > 0
    print("Test Passed!")

if __name__ == "__main__":
    test_engine()
