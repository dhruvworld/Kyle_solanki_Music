# Recommended Features for Pop vs Non-Pop Classification

## 🎯 Top Priority Features (Must Have for Pop Classification)

Based on music theory and Spotify's audio analysis, these features are **most predictive** for pop music:

### 1. **danceability** (0.0-1.0) ⭐⭐⭐⭐⭐
- **Why**: Pop music is designed to be danceable
- **Expected**: Pop tracks typically have danceability > 0.6
- **Impact**: Very high - directly captures "pop" characteristic

### 2. **energy** (0.0-1.0) ⭐⭐⭐⭐⭐
- **Why**: Pop music is typically high-energy and upbeat
- **Expected**: Pop tracks usually have energy > 0.5
- **Impact**: Very high - distinguishes from slow/ballad genres

### 3. **valence** (0.0-1.0) ⭐⭐⭐⭐⭐
- **Why**: Pop music is generally positive/happy
- **Expected**: Pop tracks typically have valence > 0.5
- **Impact**: Very high - "happy" music is a key pop trait

### 4. **acousticness** (0.0-1.0) ⭐⭐⭐⭐
- **Why**: Pop is usually electronic/produced, not acoustic
- **Expected**: Pop tracks typically have acousticness < 0.5
- **Impact**: High - distinguishes from folk/acoustic genres

### 5. **speechiness** (0.0-1.0) ⭐⭐⭐⭐
- **Why**: Helps distinguish pop songs from rap/spoken word
- **Expected**: Pop tracks typically have speechiness < 0.3
- **Impact**: High - filters out rap/hip-hop

### 6. **instrumentalness** (0.0-1.0) ⭐⭐⭐
- **Why**: Pop songs have vocals (not instrumental)
- **Expected**: Pop tracks typically have instrumentalness < 0.5
- **Impact**: Medium - helps filter instrumental tracks

### 7. **mode** (0 or 1) ⭐⭐⭐
- **Why**: Pop music often uses major keys (happier sound)
- **Expected**: Pop tracks more likely to have mode = 1 (major)
- **Impact**: Medium - subtle but useful signal

### 8. **loudness** (-60 to 0 dB) ⭐⭐⭐
- **Why**: Modern pop has specific production/loudness patterns
- **Expected**: Pop tracks typically -10 to -5 dB
- **Impact**: Medium - production style indicator

### 9. **duration_ms** (milliseconds) ⭐⭐
- **Why**: Pop songs have typical length (3-4 minutes)
- **Expected**: Pop tracks typically 180,000-240,000 ms (3-4 min)
- **Impact**: Low-Medium - length patterns

---

## 📊 Feature Priority Summary

### **Tier 1: Essential** (Add these first)
1. ✅ danceability
2. ✅ energy  
3. ✅ valence
4. ✅ acousticness

### **Tier 2: Important** (Add for better accuracy)
5. ✅ speechiness
6. ✅ instrumentalness
7. ✅ mode

### **Tier 3: Nice to Have** (Add for completeness)
8. ✅ loudness
9. ✅ duration_ms
10. key (musical key - less predictive)
11. time_signature (most pop is 4/4 - less predictive)
12. liveness (live vs studio - less predictive)

---

## 🎵 Expected Pop vs Non-Pop Patterns

| Feature | Pop Music | Non-Pop Music |
|---------|-----------|---------------|
| **danceability** | High (>0.6) | Variable |
| **energy** | High (>0.5) | Variable |
| **valence** | High (>0.5) | Variable (can be low for sad songs) |
| **acousticness** | Low (<0.5) | Variable (folk/indie can be high) |
| **speechiness** | Low (<0.3) | High for rap/hip-hop |
| **instrumentalness** | Low (<0.5) | High for instrumental genres |
| **mode** | Often Major (1) | Variable |
| **loudness** | -10 to -5 dB | Variable |

---

## 💡 Derived Features (Can Create from Audio Features)

These interaction features can be even more predictive:

1. **danceability × energy** - "Danceable and energetic" = very pop-like
2. **valence × energy** - "Happy and energetic" = classic pop
3. **is_major_key** = (mode == 1) - Binary: major vs minor
4. **song_length_min** = duration_ms / 60000 - Length in minutes
5. **is_pop_length** = (180000 <= duration_ms <= 240000) - Typical pop length
6. **energy × (1 - acousticness)** - "Energetic and electronic" = pop

---

## 🚀 Implementation Plan

1. **Fetch all 13 audio features** using `fetch_audio_features.py`
2. **Start with Tier 1 features** (danceability, energy, valence, acousticness)
3. **Add Tier 2 features** (speechiness, instrumentalness, mode)
4. **Create derived features** (interactions, binary flags)
5. **Update notebook** to use these features
6. **Compare model performance** before/after adding features

---

## 📈 Expected Impact

Adding these audio features should:
- **Improve accuracy** from ~99.9% to potentially 99.95%+
- **Better generalization** to new tracks
- **More interpretable** model (can see which musical traits matter)
- **Robust predictions** even when genre tags are missing

The combination of **danceability + energy + valence** alone should be very powerful for pop classification!

