# utils.py
def detect_anomalies(df):
    anomalies = []

    # 1. Altitude Drops
    if 'Alt' in df.columns:
        df['Alt_diff'] = df['Alt'].diff()
        sudden_drops = df[df['Alt_diff'] < -10]
        if not sudden_drops.empty:
            anomalies.append(f"Detected {len(sudden_drops)} sharp altitude drops (>10m).")

    # 2. GPS Signal Loss
    if 'GPSstatus' in df.columns:
        gps_loss = df[df['GPSstatus'] == 0]
        if not gps_loss.empty:
            anomalies.append("Detected GPS signal loss.")

    # 3. Battery Temperature
    if 'Curr' in df.columns:  # Assuming 'Curr' reflects temp or load
        if df['Curr'].max() > 40:
            anomalies.append("Battery current peaked unusually high.")

    # 4. RC Signal Loss
    if 'RCin' in df.columns:
        rc_lost = df[df['RCin'] == 0]
        if not rc_lost.empty:
            anomalies.append("RC input signal dropped at some point.")

    # 5. Mid-flight Errors (from ERR messages)
    if 'ErrMessage' in df.columns:
        errors = df['ErrMessage'].dropna().unique()
        if len(errors) > 0:
            anomalies.append(f"Errors detected: {', '.join(errors)}")

    if not anomalies:
        return "No obvious anomalies were detected."
    
    return " | ".join(anomalies)


# utils.py
def get_flight_time(df):
    if 'TimeUS' in df.columns:
        start_us = df['TimeUS'].iloc[0]
        end_us = df['TimeUS'].iloc[-1]
        duration_sec = round((end_us - start_us) / 1_000_000, 2)
        return f"The total flight time was approximately {duration_sec} seconds."
    return "Flight duration could not be determined from the log."
