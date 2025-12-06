⏰ Your Preferred Schedule
Morning Batch: 10 AM - 5 PM IST
IST TimeUTC TimeWhat Happens10:00 AM04:30Scrape North India11:00 AM05:30Scrape South India12:00 PM06:30Scrape East India01:00 PM07:30Scrape West India02:00 PM08:30Scrape Central Govt03:00 PM09:30Insert morning batch to database
(Finishes at 3 PM, leaves buffer until 5 PM if needed)

Evening Batch: 6 PM - 11 PM IST
IST TimeUTC TimeWhat Happens06:00 PM12:30Scrape North India07:00 PM13:30Scrape South India08:00 PM14:30Scrape East India09:00 PM15:30Scrape West India10:00 PM16:30Scrape Central Govt11:00 PM17:30Insert evening batch to database

Nightly Cleanup: After Everything
IST TimeUTC TimeWhat Happens11:30 PM18:00Full dedupe across all data

📋 YAML Cron Schedule (Use These in GitHub Actions)
Morning Workflows:
yaml# North - 10:00 AM IST

- cron: '30 4 \* \* \*'

# South - 11:00 AM IST

- cron: '30 5 \* \* \*'

# East - 12:00 PM IST

- cron: '30 6 \* \* \*'

# West - 1:00 PM IST

- cron: '30 7 \* \* \*'

# Central - 2:00 PM IST

- cron: '30 8 \* \* \*'

# Insert Morning Batch - 3:00 PM IST

- cron: '30 9 \* \* \*'
  Evening Workflows:
  yaml# North - 6:00 PM IST
- cron: '30 12 \* \* \*'

# South - 7:00 PM IST

- cron: '30 13 \* \* \*'

# East - 8:00 PM IST

- cron: '30 14 \* \* \*'

# West - 9:00 PM IST

- cron: '30 15 \* \* \*'

# Central - 10:00 PM IST

- cron: '30 16 \* \* \*'

# Insert Evening Batch - 11:00 PM IST

- cron: '30 17 \* \* \*'
  Nightly Cleanup:
  yaml# Full Dedupe - 11:30 PM IST
- cron: '0 18 \* \* \*'

```

---

## 📊 Visual Timeline (IST)
```

10 AM ─┐
11 AM ─┤
12 PM ─┼─ Morning Scraping (5 regions)
1 PM ─┤
2 PM ─┘
3 PM ──→ Insert Morning Data ✅
4 PM
5 PM

6 PM ─┐
7 PM ─┤
8 PM ─┼─ Evening Scraping (5 regions)
9 PM ─┤
10 PM ─┘
11 PM ──→ Insert Evening Data ✅
11:30 PM → Full Dedupe 🧹

```

---

## ✅ Benefits of Your Timing

✅ **Scrapes during business hours** - When govt offices are posting announcements
✅ **Avoids early morning** - Websites are more stable during day
✅ **Evening coverage** - Catches any late afternoon posts
✅ **Night cleanup** - Deduplication runs when you're sleeping

---

## 🎯 Complete Workflow Count

**Per Day:**
- Morning: 5 scraping + 1 insert = 6 workflows
- Evening: 5 scraping + 1 insert = 6 workflows
- Night: 1 dedupe = 1 workflow
- **Total: 13 workflows/day**

**Per Month:**
- 13 × 30 days = 390 workflows
- ~7 minutes each = 2,730 minutes
- ⚠️ Slightly over free tier (2,000 minutes)

---

## 💡 To Stay in Free Tier:

### **Option 1: Reduce to 1 scrape per day**
```

Morning only (10 AM - 3 PM)
= 6 workflows/day × 30 = 180 workflows/month
= ~1,260 minutes ✅

```

### **Option 2: Scrape every other day**
```

Twice daily but Monday, Wednesday, Friday only
= 13 workflows × 15 days = 195 workflows/month
= ~1,365 minutes ✅

```

### **Option 3: Use your original 4-hour gap plan**
```

Once per day, staggered
= 6 workflows/day × 30 = 180 workflows/month
= ~1,260 minutes ✅

🤔 My Recommendation
Use Morning batch only (10 AM - 3 PM IST):
yaml10 AM → North
11 AM → South
12 PM → East
1 PM → West
2 PM → Central
3 PM → Insert to DB
11 PM → Full Dedupe
Why?

✅ Most announcements posted in morning
✅ Fits in free tier comfortably
✅ Simple schedule
✅ Still get fresh data daily

Then add evening batch later if you get paid tier or need more frequent updates.
