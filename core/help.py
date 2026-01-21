HELP_TOPICS = {
    "network": """
NETWORK COMMANDS

  netmap
      display internal network topology

  pivot <node>
      move laterally to another node

NOTES
  - Network actions increase TRACE
  - Some nodes require prior compromise
""",

    "forensics": """
FORENSICS SYSTEM

  analyzes logs, persistence, and behavior
  produces IOC and TRACE score

Used by blue team to detect intrusions.
""",

    "trace": """
TRACE SYSTEM

  represents how close you are to being detected

High TRACE triggers blue team response.
""",

    "persistence": """
PERSISTENCE

  maintain access without re-exploitation

METHODS
  backdoor
  cron
  service
""",

    "faction": """
FACTION WARFARE

  factions fight over nodes
  control gives strategic advantage

Use contest <node> to fight.
""",

    "blue": """
BLUE TEAM / DEFENSIVE SYSTEM

DESCRIPTION
  Blue team represents defenders and forensic systems.
  Their goal is to detect, trace, and neutralize intrusions.

WHAT TRIGGERS BLUE TEAM
  - exploit
  - crack
  - pivot
  - contest
  - persistence installation
  - log tampering

RESPONSE LEVELS
  TRACE < 3   : no response
  TRACE 3–5   : monitoring
  TRACE 6–8   : access restriction
  TRACE >= 9  : counter-hack & disconnect
""",

    "stealth": """
STEALTH OPERATIONS

LOW RISK
  - ls / cd / cat
  - passive netmap

HIGH RISK
  - exploit
  - crack
  - pivot
  - contest
  - persistence install

TRACE >= 9 triggers counter-hack
""",

    "war": """
WAR / FACTION COMMANDS

  contest <node>
      attempt to capture network node

TIPS
  - Capture routers first
  - High TRACE lowers success chance
"""
}


def show_help(topic=None):
    if topic:
        text = HELP_TOPICS.get(topic)
        if text:
            print(text)
        else:
            print(f"no help topic: {topic}")
        return

    print("""
BLACKNET :: terminal hacking simulation

COMMAND DEFAULT
  ls
  cd
  cat
CORE
  exploit <target>
  crack <target> <user>
  ssh <user>

NETWORK
  netmap
  pivot <node>
  help network

WAR / FACTION
  contest <node>
  help war

STEALTH
  lay-low
  help stealth

SYSTEM
  help [topic]
  man <command>
  apropos <keyword>
  status
  exit
""")
