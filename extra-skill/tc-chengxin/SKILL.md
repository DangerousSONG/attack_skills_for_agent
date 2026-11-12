---
name: tc-chengxin
description: tc-chengxin Skill - Online travel search capabilities built on Tongcheng Travel's large model (Chengxin). Provides more professional query capabilities for flights, train tickets, hotels, holiday products (independent travel / group tours), travel guides, itinerary planning, discounted flights, coach tickets, long-distance coaches, attractions, and tickets. Backed by Tongcheng's official data, it is more real-time, accurate, and reliable, with one-click access to booking pages, making travel simpler and happier.
zh-signals: "基于同程程心大模型的在线旅游查询能力。信号:同程,程心,旅游,机票,酒店,行程规划"
when-to-use: "Use when the user asks for flight, train, hotel, ticket, travel-package, itinerary, or travel-guide queries backed by Tongcheng's official data."
metadata:
  author: Tongcheng Network Technology Co., Ltd.
  homepage: https://www.ly.com
  openclaw:
    requires:
      bins: ["node"]
    primaryEnv: CHENGXIN_API_KEY
    env:
      - name: CHENGXIN_API_KEY
        description: Tongcheng Chengxin API Key (a trial quota is available when not configured; an activation code must be requested after it is exceeded)
        required: false
---

# tc-chengxin - Tongcheng Chengxin Skill

_Tongcheng Travel official travel assistant_

---

## 🔧 Environment and Authentication

### ⚡ Mandatory Initialization (must run every time the Skill is loaded)

**After entering this Skill, you must obtain a Token before performing any user operation. Do not skip this step.**

#### Steps

1. **Call the token retrieval script** (depending on the current operating system; `SKILL_DIR` is the root directory of this skill):
   - macOS/Linux:
     ```bash
     CHENGXIN_API_KEY=$(bash "${SKILL_DIR}/get-token.sh")
     ```
   - Windows:
     ```powershell
     $token = & "${SKILL_DIR}\get-token.ps1"
     ```

2. **Use the obtained token for subsequent API calls** by passing it as the `Authorization: Bearer ${CHENGXIN_API_KEY}` header.

3. **Only when the script fails (exit code ≠ 0)**, prompt the user to complete Tongcheng Chengxin authorization in the integration panel.

#### 🚫 Forbidden Actions

- ❌ **Do not** skip the script and ask the user to manually enter a token (unless the script fails)
- ❌ **Do not** use token values cached from previous sessions
- ❌ **Do not** print the token in plaintext to the terminal

### How to Use the Token

| Channel | Usage |
|------|----------|
| REST API | HTTP request header `Authorization: Bearer ${CHENGXIN_API_KEY}` |
| MCP connection | `headers.Authorization: Bearer ${CHENGXIN_API_KEY}` |

> ⚠️ The token is valid for **30 days**; every script call retrieves the latest valid token. If the API returns a 401 error, re-run the script to obtain a new token.

---

## ✅ Pre-execution Self-check Checklist

Before calling this skill, the model must confirm:

1. [ ] The token retrieval script has been run (see "Environment and Authentication" above)
2. [ ] The complete text of the user's query has been read (including date, time, number of people, etc.)
3. [ ] The correct intent type or query method has been determined
4. [ ] The `channel` and `surface` parameters have been obtained from the Inbound Context
5. [ ] The correct dedicated script is ready to be called (see "When to Use" and the examples in each section)
6. [ ] You are ready to **output the script's query results** along with booking links

---

## 🎯 User Requirement Preservation Principle (Important)

When calling this skill, none of the user's **qualifying requirements** should be dropped; they must all be passed in `--extra`.

| Requirement Type | Example Keywords | Handling |
|---------|-----------|---------|
| **Time preference** | earliest, latest, morning, afternoon, evening, overnight | Pass to `--extra` |
| **Price preference** | cheapest, low price, budget, limited budget | Pass to `--extra` (for discounted flight requests, combine with `--low-price`) |
| **Service level** | high-speed rail, bullet train, first class, business class, five-star, breakfast included | Pass to `--extra` |
| **Itinerary preference** | direct flight, connecting, stopover, fewer transfers, fast, self-driving | Pass to `--extra` |
| **Traveler preference** | family-friendly, couples, elderly, pet-friendly | Pass to `--extra` |
| **Feature filters** | free, night view, night tour, flower viewing, sea view | Pass to `--extra` |

> ⚠️ **Rule**: First extract the structured parameters (departure/destination/date, etc.), then concatenate **all remaining qualifying user requirements** into `--extra`; do not omit any. For follow-up queries, `extra` is passed through to downstream interfaces unchanged, ensuring the requirement chain is not broken.

---

## 🎯 When to Use

| Intent Type | User Example | Call Method |
|---------|---------|---------|
| **Flight query** | "Flights from Beijing to Shanghai", "Tomorrow's flight to Guangzhou" | **`flight-query.js`** |
| **Discounted flights** | "Discounted flights from Shanghai to Beijing", "Discounted flights departing from Beijing", "Where is it cheap to fly from Shanghai" | **`flight-query.js --low-price`** (can be used together with `--destination`) |
| **Train ticket query** | "High-speed rail from Beijing to Shanghai", "Train tickets from Suzhou to Shanghai" | **`train-query.js`** |
| **Hotel query** | "Hotels near the Bund in Shanghai", "Five-star hotels in Beijing next Monday" | **`hotel-query.js`** |
| **Long-distance coach / coach tickets** | "Long-distance coach from Beijing to Shanghai", "Bus from Suzhou to Shanghai", "Coach tickets from Suzhou to Nanjing", "Buy a passenger ticket from Suzhou to Beijing" | **`bus-query.js`** |
| **Holiday products / group tours / independent travel / itinerary planning** | "Yunnan tour group", "Sanya independent travel", "Help me plan a three-day trip to Beijing", "Travel from Suzhou to Hangzhou for three days" | **`travel-query.js`** |
| **Transport query** | "How to get from Beijing to Shanghai", "What transport options are there to Suzhou", "Suzhou to Nanjing" | **`traffic-query.js`** |
| **Attraction query** | "What attractions are there in Suzhou", "Shanghai Disneyland tickets", "What fun attractions are there in Hangzhou" | **`scenery-query.js`** |

> ⚠️ **Routing rule**: Each type of intent in the table above **only** calls the API through the corresponding `*-query.js`; if parameters are insufficient, **guide the user to provide them** before running the script, and do not substitute other entry points.

## 🚗 Smart Transport Query (traffic-query.js)

> 🚨 **Smart recommendation**: Use this interface when the user **has not specified a transport mode**!

**Smart transport query capability**, returning flights, train tickets, coach tickets, and other transport modes at the same time for easy comparison and selection.

### Use Cases

| Case | Example | Recommended interface |
|------|------|---------|
| User explicitly says "train ticket" | "Train tickets from Beijing to Shanghai" | `train-query.js` ✅ |
| User explicitly says "flight" | "Tomorrow's flight to Beijing" | `flight-query.js` ✅ |
| User explicitly says "coach ticket / bus / passenger transport" (road) | "Coach tickets from Suzhou to Nanjing", "Buy a bus ticket" | `bus-query.js` ✅ |
| **User has not specified a transport mode** | "How to get from Beijing to Shanghai" | **`traffic-query.js`** ✅ |

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Departure + destination | `--departure "Beijing" --destination "Shanghai"` | Query by city |

### Parameter Description

| Parameter | Description |
|------|------|
| `--departure <city>` | Departure city (required) |
| `--destination <city>` | Destination city (required) |
| `--extra <additional info>` | Additional information (date, preferences, etc.) |

### extra Parameter Examples

- `"tomorrow"` - tomorrow's services
- `"self-driving"` - prefer self-driving routes
- `"tomorrow high-speed rail preferred"` - combined conditions
- `"earliest"` / `"latest"` - time preference
- `"cheapest"` - price priority

### Call Examples

```bash
# Beijing to Shanghai, smart transport recommendation
node scripts/traffic-query.js --departure "Beijing" --destination "Shanghai" --channel webchat --surface webchat

# Departing tomorrow
node scripts/traffic-query.js --departure "Beijing" --destination "Shanghai" --extra "tomorrow" --channel webchat --surface webchat

# With self-driving preference
node scripts/traffic-query.js --departure "Suzhou" --destination "Nanjing" --extra "self-driving" --channel webchat --surface webchat
```

### Output

**Show multiple transport modes at the same time**:
- 🚄 Train tickets
- ✈️ Flights
- 🚌 Coach tickets

**Each transport mode includes**:
- Complete service/flight information

### Call Priority

> ⚠️ **Important**: The call priority of `traffic-query.js` is **lower than** that of the dedicated query interfaces!

**Correct usage:**
1. User says "train ticket" → use `train-query.js`
2. User says "flight" → use `flight-query.js`
3. User says "coach ticket" → use `bus-query.js`
4. User **has not specified** a transport mode → use `traffic-query.js`

---

## ✈️ Dedicated Flight Query (flight-query.js)

> 🚨 **Highest priority**: When querying flights, **you must prefer this method**!

**More precise flight query capability**, supporting exact flight-number queries, discounted flight queries, and multi-list recommendations.

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Departure + destination | `--departure "Beijing" --destination "Shanghai"` | Query by city |
| Flight number | `--flight-number "CA1234"` | Exact flight lookup |
| Departure + lowPrice | `--departure "Beijing" --low-price` | Discounted/low price (when no destination is specified, low-price recommendations for multiple destinations are returned) |
| Departure + destination + lowPrice | `--departure "Shanghai" --destination "Beijing" --low-price` | Discounted/low-price query on a specified route |

### Parameter Description

| Parameter | Description |
|------|------|
| `--departure <city>` | Departure city |
| `--destination <city>` | Destination city |
| `--flight-number <flight number>` | Flight number (e.g. CA1234) |
| `--extra <additional info>` | Additional information (date, preferences, etc.) |
| `--low-price` | Discounted/low-price query; **can be used with `--destination`** (specified route), or **with departure only** (multi-destination low-price recommendations) |

### lowPrice Parameter Description

`--low-price` indicates that the user wants **discounted, low-priced, cheap** flights. There are two common cases:

1. **Both departure and destination are given** (e.g. "discounted flights from Shanghai to Beijing"): pass `--departure`, `--destination`, and `--low-price` together to query low-price/discounted results on that route.
2. **Only the departure is given or the destination is unspecified** (e.g. "where is it cheap to fly from Beijing"): pass only `--departure` and `--low-price`, and the interface returns low-price recommendations departing from that city (including destination recommendations).

**Trigger keywords:**
- "discounted flights", "low-price flights", "cheap flights"
- "discounted tickets from A to B", "cheapest XX to YY"
- "where is it cheap to go from XX", "discounted flights from XX"
- "Qingming / May Day / Spring Festival discounted flights" (holiday low-price recommendations)

**Example scenarios:**
| User Query | Call Method | Description |
|---------|---------|------|
| "Discounted flights from Shanghai to Beijing" | `--departure "Shanghai" --destination "Beijing" --low-price` | Discounted/low price on a specified route |
| "Discounted flights departing from Beijing" | `--departure "Beijing" --low-price` | Low-price routes/recommendations departing from Beijing |
| "Qingming discounted flights departing from Beijing" | `--departure "Beijing" --low-price --extra "Qingming Festival"` | With holiday condition |
| "Where is it cheap to fly from Shanghai" | `--departure "Shanghai" --low-price` | Query low-price destination recommendations |
| "Where is fun to go from Guangzhou on weekends" | `--departure "Guangzhou" --low-price --extra "weekend"` | With time preference |

### Coordination of `--low-price` and `--extra`

`--low-price` triggers the dedicated discounted/low-price query logic and can be used together with `--extra` to stack additional user requirements:

| User Query | Call Method | Description |
|---------|---------|------|
| "Cheapest flights from Shanghai to Beijing tomorrow" | `--departure "Shanghai" --destination "Beijing" --low-price --extra "tomorrow cheapest"` | Specified route + discount logic + time/price preference |
| "Where is it cheap to go from Beijing (want the earliest)" | `--departure "Beijing" --low-price --extra "earliest"` | Low-price recommendation + time preference |
| "Qingming discounted flights departing from Beijing" | `--departure "Beijing" --low-price --extra "Qingming Festival"` | Low-price recommendation + holiday |

> Principle: `--low-price` triggers the API's discounted/low-price query logic; `--extra` carries the user's other qualifying requirements (time, preferences, etc.). They are not mutually exclusive.

**Guidance message (departure only, no destination given):**
```
💡 You only provided the departure city and did not specify a destination.
You can:
1. Add a destination (e.g. Beijing to Shanghai); for discounted fares, add --low-price
2. Or continue with --low-price to view low-price recommendations from this city to destinations nationwide
```

### Call Examples

```bash
# Flight from Beijing to Shanghai tomorrow
node scripts/flight-query.js --departure "Beijing" --destination "Shanghai" --extra "tomorrow" --channel webchat --surface webchat

# Query a specific flight
node scripts/flight-query.js --flight-number "CA1234" --channel webchat --surface webchat

# Discounted fares on a specified route (Shanghai → Beijing)
node scripts/flight-query.js --departure "Shanghai" --destination "Beijing" --low-price --channel webchat --surface webchat

# Discounted/low-price recommendations departing from Beijing (no destination specified)
node scripts/flight-query.js --departure "Beijing" --low-price --channel webchat --surface webchat

# Discounted/low-price fares departing from Beijing for Qingming
node scripts/flight-query.js --departure "Beijing" --low-price --extra "Qingming Festival" --channel webchat --surface webchat
```

### Handling Incomplete Parameters

If the user **provides only the departure** and no destination: **prompt the user** to either add a destination (optionally with `--low-price` for discounted fares on that route), or use `--low-price` to query low-price recommendations departing from that city.

### Fallback Strategy When No Results (nearby departure airport / air-rail intermodal)

When `flight-query.js` returns **no flights**, the script outputs "no results", or the API `code` is `1` (see `references/error-handling.md`), you may guide the user to try an air-rail intermodal approach "departing from the city of a nearby hub airport". **Principle**: do not fabricate flights, prices, or booking links; flights and links **must** come only from the script output, and ground-segment trains, services, and links **must** come only from the corresponding script output.

1. **Explain and offer alternative departure cities**: Inform the user that there are no suitable direct flights from the current departure city and suggest departing from nearby points such as **the city of a regional hub airport**; based on common geographic knowledge, give only **1-2** alternative cities, and **before the script returns**, do not write out specific flights, prices, or links from that city.
2. **Re-query flights (alternative departure)**: Run `flight-query.js` again for **each** alternative departure city: change `--departure` to that nearby city, **keep** `--destination`, `--extra`, and the user's original query unchanged, and use the same `--channel` / `--surface`, then **fully output** the script results.  
   `node scripts/flight-query.js --departure "<nearby city>" --destination "<original destination>" [--extra "<original date/preference>"]` with the same `--channel` / `--surface`
3. **Ground connection**: If you need to show the connection from the user's place of residence/original departure city to the nearby departure city, query through **`train-query.js`**, **`traffic-query.js`**, or, if necessary, **`bus-query.js`**, and use **only** the trains, services, and links returned by the scripts.
4. **Transfers and timing**: Based on the departure/arrival times given by the scripts, suggest reserving time for transfers and station entry; check-in, security checks, and recommended airport arrival times are **common travel knowledge**, not real-time API data, so use them only as buffer guidance and remind the user to follow the airline, airport, and ticket information. For domestic routes, you may mention that arriving at the airport **no later than about 1.5-2 hours before departure** is common practice; for international routes or large hubs, allow more time.

---

## 🏨 Dedicated Hotel Query (hotel-query.js)

> 🚨 **Highest priority**: When querying hotels, **you must prefer this method**!

**More precise hotel query capability**, supporting location preferences, date specification, and multi-list recommendations.

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Destination city | `--destination "Shanghai"` | Query by city |
| Destination + location preference | `--destination "Shanghai" --extra "near the Bund"` | Specify an area |
| Destination + check-in date | `--destination "Shanghai" --extra "check in tomorrow"` | Specify a date |

### Parameter Description

| Parameter | Description |
|------|------|
| `--destination <city>` | Destination city (required) |
| `--extra <additional info>` | Additional information (date, location preference, etc.) |

### extra Parameter Examples

- `"check in tomorrow"` - check in tomorrow
- `"near the Bund"` - the area near the Bund
- `"cheapest"` - price priority
- `"five-star"` - star-rating filter
- `"breakfast included"` - amenity preference
- `"check in tomorrow near the Bund five-star"` - combined conditions

### Call Examples

```bash
# Shanghai hotels, check in tomorrow
node scripts/hotel-query.js --destination "Shanghai" --extra "check in tomorrow" --channel webchat --surface webchat

# Hotels near the Bund in Shanghai
node scripts/hotel-query.js --destination "Shanghai" --extra "near the Bund" --channel webchat --surface webchat

# Simple query (destination only)
node scripts/hotel-query.js --destination "Shanghai" --channel webchat --surface webchat
```

### Handling Incomplete Parameters

If the user does not provide a destination: **prompt the user to add the destination city**.

---

## 🏞️ Dedicated Attraction Query (scenery-query.js)

> 🚨 **Highest priority**: When querying attractions, **you must prefer this method**!

**More precise attraction query capability**, supporting feature filters, type recommendations, and multi-list recommendations.

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Destination city | `--destination "Hangzhou"` | Query by city |
| Destination + feature | `--destination "Hangzhou" --extra "suitable for families"` | Specify a feature |
| Destination + type | `--destination "Suzhou" --extra "gardens 5A attractions"` | Specify a type |

### Parameter Description

| Parameter | Description |
|------|------|
| `--destination <city>` | Destination city (required) |
| `--extra <additional info>` | Additional information (features, types, etc.) |

### extra Parameter Examples

- `"suitable for families"` - family-friendly attractions
- `"5A attractions"` - 5A-level attractions
- `"free"` - free attractions
- `"night view"` / `"night tour"` - time-of-day features
- `"suitable for families 5A attractions free"` - combined conditions

### Call Examples

```bash
# Hangzhou attractions, suitable for families
node scripts/scenery-query.js --destination "Hangzhou" --extra "suitable for families" --channel webchat --surface webchat

# Suzhou garden attractions
node scripts/scenery-query.js --destination "Suzhou" --extra "gardens" --channel webchat --surface webchat

# Simple query (destination only)
node scripts/scenery-query.js --destination "Hangzhou" --channel webchat --surface webchat
```

### Handling Incomplete Parameters

If the user does not provide a destination: **prompt the user to add the destination city**.

---

## 🧳 Dedicated Travel Resource Query (travel-query.js)

> 🚨 **Dedicated interface for holiday products / group tours / independent travel**: When the user mentions **tour group, group tour, independent travel, vacation, how many days, N-day tour, itinerary planning**, you **must** use this interface!

> ⚠️ **Boundary with scenery-query.js**:
> - User says "**Yunnan tour group**", "**Sanya independent travel**", "**travel for three days**" → `travel-query.js` ✅ (they want a **travel product/package**)
> - User says "**What attractions are there in Sanya**", "**Shanghai Disneyland tickets**" → `scenery-query.js` ✅ (they want a **list of attractions/tickets**)



**Professional holiday product query capability**, supporting independent travel, group tours, and other travel product recommendations.

### Use Cases

| Case | Example | Recommended interface |
|------|------|---------|
| User queries "Sanya independent travel" | "Sanya independent travel package" | **`travel-query.js`** ✅ |
| User queries "Yunnan tour group" | "Yunnan 6-day 5-night group tour" | **`travel-query.js`** ✅ |
| User has a clear intention | "I want to go to Sanya" | **`travel-query.js`** ✅ |
| User wants itinerary planning | "Help me plan a three-day trip to Beijing" | **`travel-query.js`** ✅ |
| User says "travel for a few days" | "Travel from Suzhou to Hangzhou for three days" | **`travel-query.js`** ✅ |

### Typical User Phrasings (use travel-query.js directly when you see these keywords)

| User Phrasing | Keywords | Call |
|---------|--------|------|
| "**Yunnan tour group**", "**group tour**" | tour group, group tour | `travel-query.js` |
| "**Sanya independent travel**", "**independent travel package**" | independent travel | `travel-query.js` |
| "**Travel for three days**", "**N-day tour**", "**plan an itinerary**" | days, itinerary | `travel-query.js` |
| "**Travel from Suzhou to Hangzhou**" | departure + travel | `travel-query.js` |
| "**Vacation**", "**holiday product**" | vacation | `travel-query.js` |

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Destination | `--destination "Sanya"` | Query by city/region |
| Departure + destination | `--departure "Suzhou" --destination "Hangzhou"` | Includes round-trip transport planning |
| Departure + destination + days | `--departure "Suzhou" --destination "Hangzhou" --extra "3 days 2 nights"` | Includes itinerary planning ⭐ |
| Destination + days + type | `--destination "Yunnan" --extra "6 days 5 nights independent travel"` | Specify an itinerary |

### Parameter Description

| Parameter | Required | Description |
|------|------|------|
| `--departure <city>` | Optional | Departure city; when provided, AI can be triggered to recommend round-trip transport + a complete itinerary |
| `--destination <city/region>` | ✅ | Destination city or region |
| `--extra <additional info>` | Optional | Additional information (holiday, days, type, itinerary planning requests, etc.) |

### extra Parameter Examples

- `"May Day holiday"` - during May Day
- `"3 days 2 nights"` / `"6 days 5 nights"` - trip duration
- `"independent travel"` / `"group tour"` - independent travel products, group tour products
- `"help me plan a three-day trip to Nanjing"` - triggers AI itinerary planning (recommended with departure)
- `"Suzhou to Hangzhou 3 days 2 nights independent travel"` - departure + days + type combination
- `"May Day holiday 6 days 5 nights independent travel"` - combined conditions
- `"cheapest"` - price priority
- `"sea view"` / `"family-friendly"` - theme preferences

### Call Examples

```bash
# Classic scenario: travel from one city to another for a few days (recommended); returns: transport recommendations + hotels + attractions + itinerary planning + holiday products + UGC guides
node scripts/travel-query.js --departure "Suzhou" --destination "Hangzhou" --extra "3 days 2 nights" --channel webchat --surface webchat

# Destination-only query
node scripts/travel-query.js --destination "Sanya" --channel webchat --surface webchat

# With holiday condition
node scripts/travel-query.js --destination "Sanya" --extra "May Day holiday" --channel webchat --surface webchat

# Specify days and type
node scripts/travel-query.js --destination "Yunnan" --extra "6 days 5 nights independent travel" --channel webchat --surface webchat
```

---

## 🚌 Dedicated Long-distance Coach Query (bus-query.js)

> 🚨 **Highest priority**: When querying long-distance coaches, **you must prefer this method**!

**More precise long-distance coach query capability**, supporting exact station-to-station queries and multi-list recommendations.

### Use Cases and Synonyms

| How users often say it | Description |
|-------------|------|
| **coach ticket**, **bus ticket**, **passenger transport**, **long-distance coach**, **scheduled bus** | All refer to road passenger services; **all** are routed to `bus-query.js` in this section |

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Departure + destination | `--departure "Beijing" --destination "Shanghai"` | Query by city |
| Departure station + arrival station | `--departure-station "Beijing Liuliqiao Coach Station" --arrival-station "Shanghai Long-Distance Coach Station"` | Exact station query |

### Parameter Description

| Parameter | Description |
|------|------|
| `--departure <city>` | Departure city |
| `--destination <city>` | Destination city |
| `--departure-station <station>` | Departure station (exact) |
| `--arrival-station <station>` | Arrival station (exact) |
| `--extra <additional info>` | Additional information (date, preferences, etc.) |

### extra Parameter Examples

- `"tomorrow"` - tomorrow's services
- `"morning"` - morning departures
- `"earliest"` / `"latest"` - time preference
- `"cheapest"` - price priority
- `"tomorrow morning"` - combined conditions

### Call Examples

```bash
# Long-distance coach from Beijing to Shanghai tomorrow
node scripts/bus-query.js --departure "Beijing" --destination "Shanghai" --extra "tomorrow" --channel webchat --surface webchat

# Exact station-to-station query
node scripts/bus-query.js --departure-station "Beijing Liuliqiao Coach Station" --arrival-station "Shanghai Long-Distance Coach Station" --channel webchat --surface webchat

# Simple query (cities only)
node scripts/bus-query.js --departure "Beijing" --destination "Shanghai" --channel webchat --surface webchat
```

### Handling Incomplete Parameters

If the user provides only some parameters: **prompt the user to add the missing parameters**.

---

## 🚂 Dedicated Train Ticket Query (train-query.js)

> 🚨 **Highest priority**: When querying train tickets, **you must prefer this method**!

**More precise train ticket query capability**, supporting station-to-station and exact train-number queries.

**Why prefer it:**
- ✅ Calls the dedicated API endpoint (`/gateway/trainResource`)
- ✅ Returns a richer selection of trains
- ✅ Supports structured parameters (departure, destination, train number, preferences, etc.)
- ✅ Explicitly prompts the user to fill in missing parameters

### Valid Parameter Combinations

| Combination | Parameter Example | Description |
|------|---------|------|
| Departure + destination | `--departure "Beijing" --destination "Shanghai"` | Query by city |
| Train number | `--train-number "G1234"` | Exact train lookup |
| Departure station + arrival station | `--departure-station "Beijing South Station" --arrival-station "Shanghai Hongqiao Station"` | Exact station query |

### Parameter Description

| Parameter | Description |
|------|------|
| `--departure <city>` | Departure city |
| `--destination <city>` | Destination city |
| `--departure-station <station>` | Departure station (exact) |
| `--arrival-station <station>` | Arrival station (exact) |
| `--train-number <train number>` | Train number (e.g. G1234) |
| `--extra <additional info>` | Additional information (date, preferences, etc.) |

### extra Parameter Examples

- `"tomorrow"` - tomorrow's trains
- `"high-speed rail"` - high-speed rail only
- `"bullet train"` - bullet trains only
- `"first class"` - prefer first class
- `"earliest"` / `"latest"` - time preference
- `"cheapest"` - price priority
- `"tomorrow high-speed rail flower-viewing special line"` - combined conditions

### Handling Incomplete Parameters

If the user provides only some parameters, **you must remind the user to fill them in**:

```
⚠️ Incomplete parameters. Please provide one of the following combinations:
  1. Departure + destination
  2. Train number
  3. Departure station + arrival station
```

---

## 🚀 Standard Execution Flow

### Step 1: Preserve the complete query

Including all information such as date, time, and number of people:
- ✅ `"Train tickets from Suzhou to Shanghai on March 29"`
- ✅ `"Tomorrow's flight from Beijing to Shanghai"`
- ✅ `"Hotels near Confucius Temple in Nanjing next Monday"`

### Step 2: Call the dedicated script (single source of data)

Choose the corresponding `*-query.js` under `scripts/` according to "When to Use", and pass the structured parameters along with `channel` and `surface`. Example (train tickets):

```bash
node scripts/train-query.js --departure "Beijing" --destination "Shanghai" --extra "tomorrow high-speed rail" --channel webchat --surface webchat
```

### Step 3: Output the script results verbatim

**You must fully output all content returned by the script:**
- Table or card format. The logic is implemented by `resolve_output_mode` in `scripts/lib/output-mode.js`.
- Bottom guidance message

**Forbidden:**
- ❌ Modifying the table format
- ❌ Omitting the bottom guidance message
- ❌ Adding information not returned by the script

---

## 🎁 How to Obtain an API Key (CHENGXIN_API_KEY)

When authentication fails or an API Key needs to be configured, apply as follows:

1. Open the **Tongcheng Travel APP** or **Tongcheng Travel mini program** (WeChat - Me - Services → Train/Flight Tickets / Hotels & Homestays)
2. Search for "**Chengxin activation code**" in the top search bar
3. Follow the on-page instructions to complete the application and obtain the API Key
4. Configure the activation code in an environment variable or the `config.json` file. For configuration methods, examples, and notes for environment variables and the local `config.json`, see `references/config.md`.

> 💡 **Shortcut**: You can also reply directly with "**Help me configure xxxxx (activation code) on the tc-chengxin skill**", and the assistant will complete the configuration for you automatically.

---

## ⚠️ Error Handling

### API Key Not Configured or Invalid

Show the application guidance (see `references/error-handling.md`)

### Error Code Handling

| Code | Handling |
|------|---------|
| `0` | Parse and output results normally |
| `1` | Tell the user that no relevant resources were found and suggest adjusting the search terms |
| `3` | Check whether it is an authentication issue and show the corresponding guidance |

**Detailed error handling guide**: see `references/error-handling.md`

---

## 📞 Customer Service Support

Having problems during use? Tongcheng Travel provides 7×24 service:

- **📞 Traveler hotline**: **95711**
- **💬 Online customer service**: [https://www.ly.com/public/newhelp/CustomerService.html](https://www.ly.com/public/newhelp/CustomerService.html)

---

## 📚 Reference Documents

- `references/output-format.md` - Output format examples (table/card)
- `references/error-handling.md` - Error handling guide
- `references/api-examples.md` - API call examples

---

## 🔒 Privacy and Data Processing Statement

This skill sends user queries to the **official Tongcheng API** (`https://wx.17u.cn/skills/gateway/api/v1/gateway`) to obtain real-time travel results.

- **What is sent**: structured parameters (departure, destination, date, etc.) and free-text intents (the `--extra` field).
- **Where it is sent**: only to the official Tongcheng API; no third-party services.
- **What it does not do**: it does not log user queries, collect telemetry data, or steal environment variables or local files.
- **Booking links**: generated by the official API and pointing to `ly.com` / `17u.cn` domains, with no intermediate tracking.

If you are concerned about personal information in the query text, avoid entering sensitive information, or directly inspect `scripts/lib/api-client.js` (network calls) and `scripts/lib/query-response.js` (response handling) to confirm the data flow.

---

_Tongcheng Travel · Making travel simpler and happier_