import pynmea2


def parse_gprmc(sentence, device_name="GPS"):
    sentence = sentence.strip()

    print(f"\n{'=' * 50}")
    print(device_name)
    print(f"{'=' * 50}")

    try:
        # Validate checksum
        msg = pynmea2.parse(sentence, check=True)

        if msg.sentence_type != "RMC":
            print("NMEA: INVALID - not RMC")
            return

        # RMC validity
        valid = msg.status == "A"

        print(f"NMEA: {'VALID' if valid else 'INVALID'}")
        print(f"Time:      {msg.timestamp}")
        print(f"Date:      {msg.datestamp}")
        print(f"Latitude:  {msg.latitude}")
        print(f"Longitude: {msg.longitude}")
        print(f"Speed:     {msg.spd_over_grnd} knots")
        print(f"Course:    {msg.true_course}°")

        # Parse optional fields directly
        fields = sentence.split(",")

        # Mode Indicator
        if len(fields) > 12:
            print(f"Mode:      {fields[12]}")

        # Navigation Status
        if len(fields) > 13:
            print(f"Nav Status: {fields[13].split('*')[0]}")

        # Validity check
        print(f"RMC Valid?: {msg.is_valid}")

        print("Checksum:  VALID")

    except pynmea2.ChecksumError:
        print("NMEA: INVALID")
        print("Reason: Checksum error")

    except pynmea2.ParseError as e:
        print("NMEA: INVALID")
        print(f"Reason: Parse error: {e}")

    except Exception as e:
        print("NMEA: INVALID")
        print(f"Reason: {type(e).__name__}: {e}")


parse_gprmc(
    "$GPRMC,135518.00,A,4725.133799,N,00921.301803,E,0.0,175.9,200826,0.1,W,A,V*52",
    "IR1833"
)

parse_gprmc(
    "$GPRMC,043240.0,A,4725.143777,N,00921.293977,E,0.0,0.0,190826,0.1,W,A*1D",
    "IR829"
)
