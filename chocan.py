from chocan import storage_system, output_system, ui_system

def main():
    storage_system.init()
    output_system.display("\nChocAn System v0.1")
    ui_system.run_ui()

if __name__ == "__main__":
    main()

