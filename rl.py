from db import get_conn

ALPHA = 0.1  # learning rate

def sample_variant():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prompt_variants")
    variants = cur.fetchall()
    conn.close()
    import random
    total = sum(v["weight"] for v in variants)
    if total == 0:
        weights = [1 for _ in variants]
    else:
        weights = [v["weight"] / total for v in variants]
    chosen = random.choices(variants, weights=weights, k=1)[0]
    return dict(chosen)

def update_variant_feedback(variant_id: int, rating: int):
    normalized = (rating - 3) / 2  # maps 1..5 to -1..1
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT weight FROM prompt_variants WHERE id = ?", (variant_id,))
    row = cur.fetchone()
    if not row:
        return
    old_weight = row["weight"]
    new_weight = old_weight * (1 + ALPHA * normalized)
    if new_weight < 0.1:
        new_weight = 0.1
    cur.execute("UPDATE prompt_variants SET weight = ? WHERE id = ?", (new_weight, variant_id))
    cur.execute("INSERT INTO reward_history (variant_id, feedback_score) VALUES (?, ?)", (variant_id, normalized))
    conn.commit()
    conn.close()
