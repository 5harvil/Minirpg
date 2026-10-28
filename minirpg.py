import mysql.connector
import random

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="groots",
    database="mini_rpg"
)

cursor = connection.cursor()

print("================================")
print("       REALM OF LEGENDS")
print("================================")

name = input("Enter your hero name: ")

cursor.execute(
    "SELECT * FROM players WHERE player_name = %s",
    (name,)
)

player = cursor.fetchone()

if player is None:
    cursor.execute(
        "INSERT INTO players (player_name) VALUES (%s)",
        (name,)
    )
    connection.commit()

    cursor.execute(
        "SELECT * FROM players WHERE player_name = %s",
        (name,)
    )
    player = cursor.fetchone()

print("\nWelcome,", name)

while True:

    cursor.execute(
        "SELECT health, xp, gold, current_level "
        "FROM players WHERE player_name = %s",
        (name,)
    )

    player = cursor.fetchone()

    health = player[0]
    xp = player[1]
    gold = player[2]
    level = player[3]

    print("\n========== HERO STATUS ==========")
    print("Name:", name)
    print("Health:", health)
    print("XP:", xp)
    print("Gold:", gold)
    print("Level:", level)
    print("=================================")

    if level > 2:
        print("YOU HAVE COMPLETED THE GAME!")
        break

    if health <= 0:
        print("Your hero has fallen. Game over!")
        break

    cursor.execute(
        "SELECT monster_id, monster_name, health, "
        "attack_power, xp_reward, gold_reward "
        "FROM monsters WHERE monster_level = %s",
        (level,)
    )

    monster = cursor.fetchone()

    monster_id = monster[0]
    monster_name = monster[1]
    monster_health = monster[2]
    monster_attack = monster[3]
    xp_reward = monster[4]
    gold_reward = monster[5]

    print("\nLocation:", "Forest" if level == 1 else "Dungeon")
    print("Enemy:", monster_name)
    print("Enemy health:", monster_health)

    input("\nPress Enter to begin battle...")

    while monster_health > 0 and health > 0:

        print("\n1. Attack")
        print("2. Drink potion (+20 health)")
        action = input("Choose action: ")

        if action == "1":

            damage = random.randint(12, 22)
            monster_health -= damage

            print("You dealt", damage, "damage!")

            if monster_health > 0:
                health -= monster_attack
                print(monster_name, "attacks!")
                print("You lost", monster_attack, "health.")

        elif action == "2":

            health = min(100, health + 20)
            print("You restored health to", health)

            health -= monster_attack
            print(monster_name, "attacks!")
            print("You lost", monster_attack, "health.")

        else:
            print("Invalid action!")
            continue

        print("Your health:", health)
        print("Enemy health:", max(0, monster_health))

    if health <= 0:

        cursor.execute(
            "UPDATE players SET health = 0 "
            "WHERE player_name = %s",
            (name,)
        )
        connection.commit()

        print("\nGAME OVER!")
        break

    print("\nYou defeated", monster_name, "!")

    xp += xp_reward
    gold += gold_reward
    level += 1

    cursor.execute(
        "UPDATE players SET health = %s, xp = %s, "
        "gold = %s, current_level = %s "
        "WHERE player_name = %s",
        (health, xp, gold, level, name)
    )

    connection.commit()

    print("XP earned:", xp_reward)
    print("Gold earned:", gold_reward)

    if level <= 2:
        print("\nThe next level awaits!")

print("\nThanks for playing!")

cursor.close()
connection.close()
