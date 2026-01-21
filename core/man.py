def man(cmd):
    pages = {

"ls": """
NAME
  ls - list directory contents

SYNOPSIS
  ls

DESCRIPTION
  Lists files in current directory.

STEALTH
  Low risk, no TRACE increase.
""",

"cd": """
NAME
  cd - change directory

SYNOPSIS
  cd <dir>

DESCRIPTION
  Changes current working directory.

STEALTH
  Safe operation.
""",

"cat": """
NAME
  cat - read file contents

SYNOPSIS
  cat <file>

DESCRIPTION
  Reads and displays file contents.

RISK
  Low trace if sensitive file accessed.
""",

# ================= CORE =================

"ssh": """
NAME
  ssh - remote login

SYNOPSIS
  ssh <user>

DESCRIPTION
  Attempts to log into a remote host.
  Success depends on credentials and trust.

RISK
  Medium TRACE on failure.
""",

"crack": """
NAME
  crack - brute-force authentication service

SYNOPSIS
  crack <target> <user>

DESCRIPTION
  Performs brute-force attack against a service
  such as ssh, ftp, or database login.

SUPPORTED SERVICES
  ssh
  ftp
  mysql

RISK
  High TRACE increase.
  May trigger BLUE TEAM response.

DETECTION
  - multiple auth failures
  - auth.log anomalies

EXAMPLE
  crack ssh
""",

"exploit": """
NAME
  exploit - exploit remote system

SYNOPSIS
  exploit <target>

DESCRIPTION
  Launch multi-stage exploit chain against target.

STAGES
  1. reconnaissance
  2. initial access
  3. privilege escalation

RISK
  Each stage increases TRACE.
  Failure aborts chain.

EXAMPLE
  exploit alpha
""",

# ================= NETWORK =================

"netmap": """
NAME
  netmap - internal network map

SYNOPSIS
  netmap

DESCRIPTION
  Display discovered internal topology, node status,
  OS, trust level, and ownership.
""",

"pivot": """
NAME
  pivot - lateral movement

SYNOPSIS
  pivot <node>

DESCRIPTION
  Move to another node inside internal network.
  Often detected by forensics.
""",

# ================= STEALTH / TRACE =================

"trace": """
NAME
  trace - detection level

DESCRIPTION
  Trace represents how visible your actions are.

LEVELS
  0–2   LOW
  3–5   MEDIUM
  6–8   HIGH
  9+    CRITICAL

CRITICAL
  TRACE >= 9 triggers blue team response.
""",

"stealth": """
NAME
  stealth - operational stealth and trace control

DESCRIPTION
  Stealth determines how detectable your actions are.

HIGH RISK ACTIONS
  exploit
  crack
  pivot
  contest
  persistence install

LOW RISK ACTIONS
  ls, cd, cat
  passive netmap

BEST PRACTICES
  - Avoid repeated exploits
  - Let TRACE cool down
  - Prefer persistence over brute force

WARNING
  CRITICAL TRACE triggers counter-hack.
""",

# ================= DEFENSE =================

"forensics": """
NAME
  forensics - defensive analysis system

DESCRIPTION
  Analyzes logs, persistence, and behavior.
  Produces detection score and IOC list.
""",

"blue": """
NAME
  blue - defensive response system

DESCRIPTION
  Represents defenders monitoring the network.

FUNCTIONS
  - detection
  - trace escalation
  - counter-hack
""",

# ================= PERSISTENCE =================

"persist": """
NAME
  persist - install persistence

SYNOPSIS
  persist backdoor|cron|service

DESCRIPTION
  Install persistence mechanisms to maintain access.
""",

"persistence": """
NAME
  persistence - maintain long-term access

METHODS
  backdoor   low noise
  cron       medium noise
  service    high risk

COMMANDS
  persist backdoor
  persist cron
  persist service
  reconnect

DETECTION
  - cron jobs
  - system services
  - startup anomalies
""",

# ================= WAR / FACTION =================

"faction": """
NAME
  faction - hacker group affiliation

DESCRIPTION
  Each player belongs to a faction (RED / BLUE).
  Factions compete over network nodes.

MECHANICS
  - Nodes have owners
  - contest used to capture
  - Wars increase TRACE

SEE ALSO
  contest, netmap
""",

"war": """
NAME
  war - faction warfare system

DESCRIPTION
  Persistent faction warfare over network nodes.

COMMANDS
  contest <node>

IMPACT
  - Increases TRACE
  - Triggers blue team escalation
""",

"contest": """
NAME
  contest - faction war command

SYNOPSIS
  contest <node>

DESCRIPTION
  Attempt to capture node for your faction.

NOTES
  Already owned nodes cannot be contested.
""",

# ================= COMMUNITY =================

"jobs": """
NAME
  jobs - list available contracts

DESCRIPTION
  Displays community or faction jobs.
""",

"take": """
NAME
  take - accept a job

SYNOPSIS
  take <job_id>

DESCRIPTION
  Accepts a job and tracks progress.
""",

"sync": """
NAME
  sync - synchronize world state

SYNOPSIS
  sync

DESCRIPTION
  Sync jobs, network and faction data.
"""
    }

    print(pages.get(cmd, "No manual entry for this command."))
