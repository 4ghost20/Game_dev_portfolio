import os

# --- Your devices ---
HDMI_SINK = "alsa_output.pci-0000_03_00.1.pro-output-7"
SPEAKER_SINK = "alsa_output.pci-0000_03_00.6.analog-stereo"
HEADSET_SINK = "bluez_output.45_69_77_86_8C_76.1"

def switch_audio(sink, label):
    os.system(f"pactl set-default-sink {sink} && "
              f"pactl list short sink-inputs | cut -f1 | "
              f"xargs -I{{}} pactl move-sink-input {{}} {sink}")
    print(f"Switched to {label}")

def main():
    while True:
        print("\nAudio Switch Menu:")
        print("1. Switch to HDMI (TV)")
        print("2. Switch to Laptop Speakers")
        print("3. Switch to Headset")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            switch_audio(HDMI_SINK, "HDMI (TV)")
        elif choice == "2":
            switch_audio(SPEAKER_SINK, "Laptop Speakers")
        elif choice == "3":
            switch_audio(HEADSET_SINK, "Headset")
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
