# Step 1.2: Core Nouns & Keyword Planner Test Seeding

This file isolates our core service nouns, picks 15 targeted test cities, and programmatically combines them into long-tail search phrases. 

You can copy and paste the compiled phrases directly into **Google Keyword Planner** to analyze their Cost Per Click (CPC) and monthly search volumes.

---

## 1. Extracted Core Service Nouns
These represent the commercial nouns and size configurations users search for in this niche:
*   `dumpster rental`
*   `roll off dumpster`
*   `construction dumpster`
*   `commercial dumpster`
*   `residential dumpster`
*   `10 yard dumpster`
*   `20 yard dumpster`
*   `30 yard dumpster`
*   `40 yard dumpster`

---

## 2. Selected Test Cities (15 Markets)
A diverse sample of major metropolitan areas representing high-volume regions across the U.S.:
1.  `austin tx`
2.  `phoenix az`
3.  `miami fl`
4.  `dallas tx`
5.  `houston tx`
6.  `los angeles ca`
7.  `san diego ca`
8.  `orlando fl`
9.  `chicago il`
10. `atlanta ga`
11. `charlotte nc`
12. `denver co`
13. `seattle wa`
14. `boston ma`
15. `philadelphia pa`

---

## 3. Programmatic Combination Matrix

Here is the simple logic used to generate our test query phrases:

```python
nouns = ["10 yard dumpster rental", "20 yard dumpster rental", "cheap dumpster rental", "roll off dumpster rental"]
cities = ["austin tx", "phoenix az", "miami fl", "dallas tx", "houston tx", "los angeles ca", "san diego ca", "orlando fl", "chicago il", "atlanta ga", "charlotte nc", "denver co", "seattle wa", "boston ma", "philadelphia pa"]

# Combination formulas:
# Form 1: [Noun] cost in [City]
# Form 2: [Noun] in [City]
```

---

## 4. Combined Test Phrases (Ready to Paste)

Copy the block below and paste it directly into **Google Keyword Planner** (`Discover new keywords` -> `Start with keywords` or `Get search volume and forecasts`):

```text
10 yard dumpster rental cost in austin tx
10 yard dumpster rental cost in phoenix az
10 yard dumpster rental cost in miami fl
10 yard dumpster rental cost in dallas tx
10 yard dumpster rental cost in houston tx
10 yard dumpster rental cost in los angeles ca
10 yard dumpster rental cost in san diego ca
10 yard dumpster rental cost in orlando fl
10 yard dumpster rental cost in chicago il
10 yard dumpster rental cost in atlanta ga
10 yard dumpster rental cost in charlotte nc
10 yard dumpster rental cost in denver co
10 yard dumpster rental cost in seattle wa
10 yard dumpster rental cost in boston ma
10 yard dumpster rental cost in philadelphia pa
cheap dumpster rental in austin tx
cheap dumpster rental in phoenix az
cheap dumpster rental in miami fl
cheap dumpster rental in dallas tx
cheap dumpster rental in houston tx
cheap dumpster rental in los angeles ca
cheap dumpster rental in san diego ca
cheap dumpster rental in orlando fl
cheap dumpster rental in chicago il
cheap dumpster rental in atlanta ga
cheap dumpster rental in charlotte nc
cheap dumpster rental in denver co
cheap dumpster rental in seattle wa
cheap dumpster rental in boston ma
cheap dumpster rental in philadelphia pa
20 yard roll off dumpster cost in austin tx
20 yard roll off dumpster cost in phoenix az
20 yard roll off dumpster cost in miami fl
20 yard roll off dumpster cost in dallas tx
20 yard roll off dumpster cost in houston tx
20 yard roll off dumpster cost in los angeles ca
20 yard roll off dumpster cost in san diego ca
20 yard roll off dumpster cost in orlando fl
20 yard roll off dumpster cost in chicago il
20 yard roll off dumpster cost in atlanta ga
20 yard roll off dumpster cost in charlotte nc
20 yard roll off dumpster cost in denver co
20 yard roll off dumpster cost in seattle wa
20 yard roll off dumpster cost in boston ma
20 yard roll off dumpster cost in philadelphia pa
```
