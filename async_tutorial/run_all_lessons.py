#!/usr/bin/env python3
"""
Run all async tutorial lessons in sequence.
"""

import asyncio
import sys
import importlib.util


def load_lesson(lesson_file: str):
    """Dynamically load a lesson module"""
    spec = importlib.util.spec_from_file_location("lesson", lesson_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {lesson_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    """Run all lessons"""
    lessons = [
        ("01_sync_basics.py", "Synchronous Programming Basics"),
        ("02_event_loop_explained.py", "The Event Loop Explained"),
        ("03_async_fundamentals.py", "Async/Await Fundamentals"),
        ("04_threading_vs_async.py", "Threading vs Async"),
    ]

    print("\n" + "=" * 70)
    print("  🎓 ASYNC/SYNC PROGRAMMING MASTERCLASS")
    print("=" * 70)
    print(f"\n  Total Lessons: {len(lessons)}")
    print("\n  Lessons:")
    for i, (file, title) in enumerate(lessons, 1):
        print(f"    {i}. {title}")

    print("\n" + "=" * 70)

    choice = (
        input("\n  Run all lessons? (y/n) or enter lesson number: ").strip().lower()
    )

    if choice == "y":
        for i, (file, title) in enumerate(lessons, 1):
            print(f"\n\n{'=' * 70}")
            print(f"  STARTING LESSON {i}: {title}")
            print("=" * 70)
            input("\nPress Enter to start...")

            try:
                module = load_lesson(file)
                if hasattr(module, "main"):
                    if asyncio.iscoroutinefunction(module.main):
                        asyncio.run(module.main())
                    else:
                        module.main()
            except KeyboardInterrupt:
                print("\n\n⏸️  Interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error in lesson: {e}")
                if input("\nContinue to next lesson? (y/n): ").lower() != "y":
                    break
    elif choice.isdigit():
        lesson_num = int(choice) - 1
        if 0 <= lesson_num < len(lessons):
            file, title = lessons[lesson_num]
            print(f"\n\n{'=' * 70}")
            print(f"  RUNNING LESSON {lesson_num + 1}: {title}")
            print("=" * 70)

            module = load_lesson(file)
            if hasattr(module, "main"):
                if asyncio.iscoroutinefunction(module.main):
                    asyncio.run(module.main())
                else:
                    module.main()
        else:
            print("❌ Invalid lesson number")
    else:
        print("Exiting...")

    print("\n\n" + "=" * 70)
    print("  🎉 TUTORIAL COMPLETE!")
    print("=" * 70)
    print("\n  📚 Additional Resources:")
    print("    - QUICK_REFERENCE.py  → Cheat sheet")
    print("    - Each lesson can be run independently")
    print("\n  Happy coding! 🚀\n")


if __name__ == "__main__":
    main()
