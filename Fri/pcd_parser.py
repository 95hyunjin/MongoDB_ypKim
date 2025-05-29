def parse_pcd(filepath):
    points = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        data_started = False
        for line in lines:
            if data_started:
                parts = line.strip().split()
                if len(parts) >= 3:
                    points.append({
                        "x": float(parts[0]),
                        "y": float(parts[1]),
                        "z": float(parts[2])
                    })
            if line.strip().lower() == 'data ascii':
                data_started = True
    return points