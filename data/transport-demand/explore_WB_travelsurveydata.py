import pandas as pd
import matplotlib.pyplot as plt

# import stata file
df = pd.read_stata(f'./../WB_travelsurvey.dta')

# transport Qs are mode to work and time to work

main_mode_cols = ['age_1', 'age_2', 'age_3', 'age_4', 'age_5', 'age_6', 'age_7', 'age_8', 'age_9', 'age_10', 'age_11',
                  'age_12', 'age_13', 'age_14', 'age_15',
                  'q14d_1', 'q14d_2', 'q14d_3', 'q14d_4', 'q14d_5', 'q14d_6', 'q14d_7', 'q14d_8', 'q14d_9', 'q14d_10',
                  'q14d_11', 'q14d_12', 'q14d_13', 'q14d_14', 'q14d_15',
                  'q14l_1', 'q14l_2', 'q14l_3', 'q14l_4', 'q14l_5', 'q14l_6', 'q14l_7', 'q14l_8', 'q14l_9', 'q14l_10',
                  'q14l_11', 'q14l_12', 'q14l_13', 'q14l_14', 'q14l_15', 'q14l_1_99', 'q14l_2_99', 'q14l_3_99',
                  'q14l_4_99', 'q14l_5_99', 'q14l_6_99', 'q14l_7_99', 'q14l_8_99', 'q14l_9_99', 'q14l_10_99',
                  'q14l_11_99', 'q14l_12_99', 'q14l_13_99', 'q14l_14_99', 'q14l_15_99', 'q14m_1', 'q14m_2', 'q14m_3',
                  'q14m_4', 'q14m_5', 'q14m_6', 'q14m_7', 'q14m_8', 'q14m_9', 'q14m_10', 'q14m_11', 'q14m_12',
                  'q14m_13', 'q14m_14', 'q14m_15']

# narrow down to transport stuff
df = df[main_mode_cols]

values = {'Walk': 0,
          'Microbus/Matatu': 0,
          'Bodaboda (Bicycle taxi)': 0,
          'Other, specify': 0,
          'Own bicycle': 0,
          'Own vehicle': 0,
          'Bus regular': 0,
          'Taxi (vehicle)': 0,
          'Shared taxi': 0}

# Count school trips by mode
for mode in values:
    for q in range(1, 16):
        values[mode] += len(df[(df[f'q14l_{q}'] == mode) & (df[f'q14d_{q}'] == 'Currently attending')])

print(values)

# Count total number of students
print(sum(values.values()))

# Count work commute trips by mode
for mode in values:
    for q in range(1, 16):
        values[mode] += len(df[(df[f'q14l_{q}'] == mode) & (df[f'q14d_{q}'] != 'Currently attending')])

print(values)
# Count total number of commuting workers
print(sum(values.values()))

# Count total number of people in this survey
people = 0
for x in range(1, 16):
    people += len(df[df[f'age_{x}'] > 0])
print(people)

# Count total number of students
students = 0
for y in range(1, 16):
    students += len(df[df[f'q14d_{y}'] == 'Currently attending'])
print(students)

# Calculate total trip time in hours of each transport mode
triptime = {'Walk': 0,
            'Microbus/Matatu': 0,
            'Bodaboda (Bicycle taxi)': 0,
            'Other, specify': 0,
            'Own bicycle': 0,
            'Own vehicle': 0,
            'Bus regular': 0,
            'Taxi (vehicle)': 0,
            'Shared taxi': 0}

for d in range(1, 16):
    df[f'q14m_{d}'] = df[f'q14m_{d}'].clip(lower=0)

for mode in triptime:
    for a in range(1, 16):
        triptime[mode] += df.loc[df[f'q14l_{a}'] == mode, f'q14m_{a}'].sum() / 60

print(triptime)

# Calculate total trip distance in miles
speed = {'Walk': 3,
         'Microbus/Matatu': 20,
         'Bodaboda (Bicycle taxi)': 15,
         'Other, specify': 15,
         'Own bicycle': 10,
         'Own vehicle': 30,
         'Bus regular': 20,
         'Taxi (vehicle)': 30,
         'Shared taxi': 30}

# {key: triptime[key]*speed[key] for key in triptime}

# Create new columns of travel speed in mph
for b in range(1, 16):
    df[f'speed_{b}'] = df[f'q14l_{b}'].map(speed)

# Create new columns of travel distance of each individual
df['speed_9'] = df['speed_9'].astype('float64')
df['speed_10'] = df['speed_10'].astype('float64')
df['speed_11'] = df['speed_11'].astype('float64')
df['speed_12'] = df['speed_12'].astype('float64')
df['speed_13'] = df['speed_13'].astype('float64')
df['speed_14'] = df['speed_14'].astype('float64')
df['speed_15'] = df['speed_15'].astype('float64')

for c in range(1, 16):
    df[f'tripdist_{c}'] = df[f'speed_{c}'] * df[f'q14m_{c}'] / 60

# Calculate total trip distance in each trip length bucket
tripdistance1 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance1:
    for e in range(1, 16):
        tripdistance1[mode] += df.loc[(df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] <= 1), f'tripdist_{e}'].sum()
print(tripdistance1)

# Repeat for all other trip length buckets
tripdistance2 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance2:
    for e in range(1, 16):
        tripdistance2[mode] += df.loc[
            (df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 1) & (df[f'tripdist_{e}'] <= 2), f'tripdist_{e}'].sum()
print(tripdistance2)

tripdistance3 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance3:
    for e in range(1, 16):
        tripdistance3[mode] += df.loc[
            (df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 2) & (df[f'tripdist_{e}'] <= 5), f'tripdist_{e}'].sum()
print(tripdistance3)

tripdistance4 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance4:
    for e in range(1, 16):
        tripdistance4[mode] += df.loc[
            (df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 5) & (df[f'tripdist_{e}'] <= 10), f'tripdist_{e}'].sum()

print(tripdistance4)

tripdistance5 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance5:
    for e in range(1, 16):
        tripdistance5[mode] += df.loc[
            (df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 10) & (df[f'tripdist_{e}'] <= 25), f'tripdist_{e}'].sum()

print(tripdistance5)

tripdistance6 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance6:
    for e in range(1, 16):
        tripdistance6[mode] += df.loc[
            (df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 25) & (df[f'tripdist_{e}'] <= 50), f'tripdist_{e}'].sum()

print(tripdistance6)

tripdistance7 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance7:
    for e in range(1, 16):
        tripdistance7[mode] += df.loc[(df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 50) & (
                    df[f'tripdist_{e}'] <= 100), f'tripdist_{e}'].sum()

print(tripdistance7)

tripdistance8 = {'Walk': 0,
                 'Microbus/Matatu': 0,
                 'Bodaboda (Bicycle taxi)': 0,
                 'Other, specify': 0,
                 'Own bicycle': 0,
                 'Own vehicle': 0,
                 'Bus regular': 0,
                 'Taxi (vehicle)': 0,
                 'Shared taxi': 0}

for mode in tripdistance8:
    for e in range(1, 16):
        tripdistance8[mode] += df.loc[(df[f'q14l_{e}'] == mode) & (df[f'tripdist_{e}'] > 100), f'tripdist_{e}'].sum()

print(f'tripdistance8{tripdistance8}')
