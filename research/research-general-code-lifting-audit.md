# Direct code lifting: audit and collision-sensitive pruning

Auxiliary research note, 18 October 2026. The article is unchanged.

**Status.** A supplied code for a subset can be executed directly on the whole hypothesis set. This is an actual partial policy, with no membership query assumed. The basic lifting bound is correct. Two stronger executable pruning bounds are proved here: a load threshold removes the height penalty when the core is large, and a collision-entropy bound handles many outsiders concentrated on few code outputs. The latter extends to weighted completion prizes. These are polynomial constructive primitives, not an unrestricted approximation theorem.

## 1. Basic lifting and the exact depth-cut profile

Let `C subset H` be a known core of `N` hypotheses and let `u=|H minus C|`. Let `B` be a supplied proper code identifying `C`, using the original tests. Its raw core cost is `F_C=sum_{h in C} depth_B(h)` and its height is `L`.

Run the queries of `B` on all of `H`. At a response branch containing no core hypothesis, stop unfinished. At a core leaf `h`, identify `h` only if no outsider reaches that leaf; otherwise stop unfinished. All routing is determined by the supplied response table and can be computed in polynomial time.

If `c` core leaves are contaminated, at least `N-c` core hypotheses finish. The work is exactly

    F_C + sum_{x outside C} number of queries routed to x,

and is at most `F_C+uL`. For nonnegative completion prizes `w_h`, the finished prize is at least `sum_C w_h` minus the sum of the `c` largest core prizes. The policy does not have to distinguish outsiders from one another in order to stop unfinished.

There is a sharper profile for every nonnegative integer cut depth `t`. Run `B` until depth `t`. Stop unfinished at every frontier cell containing outsiders, and fully execute `B` only in clean frontier cells. At contaminated core leaves reached earlier, stop unfinished. Empty-core responses also stop unfinished immediately.

Let `c_t` be the core population in the contaminated depth-`t` frontier cells, plus the number of contaminated core leaves reached earlier. Let `b_t` be the corresponding sum of core prizes. The policy has

    completed count >= N-c_t,
    completed prize >= sum_C w_h-b_t,
    work <= F_C+u t.                                          (1)

Core work only decreases under pruning. No outsider receives more than `t` queries. Scanning all `t<=L` is polynomial. Exact prefix pricing on the lifted template can only improve this explicit candidate family.

For a proper binary code, every outsider ends at a core leaf. For more than two responses, a missing-response exit can occur after the cut depth and still contaminate a frontier cell. Thus counting only occupied **core** leaves is insufficient for a balanced-tree bound in that model. One can instead count all occupied terminal routing outputs, including missing-response exits, or keep the exact profile (1). The general entropy theorem below uses the extended terminal routing outputs and covers this case explicitly.

## 2. Load-threshold pruning

This lemma was proposed independently by the credit-relaxation agent and audited here. Fix `0<alpha<=1`. At a code node `v`, let `n_v` be its core population and `u_v` its outsider population. Stop unfinished before querying any node for which

    u_v >= alpha n_v.                                       (2)

Apply (2) to leaves as well; in particular every contaminated core leaf is stopped because `u_v>=1>=alpha n_v` there. Execute a test only at nodes failing (2).

The stopped core-containing cells are disjoint. Every such cell sacrifices at most `u_v/alpha` core hypotheses, and their outsider populations sum to at most `u`. Hence at least `N-u/alpha` core hypotheses complete. At every queried node, `u_v<alpha n_v`, so

    work <= (1+alpha) sum_queried n_v
         <= (1+alpha) F_C.                                 (3)

For `alpha=1`, this completes at least `N-u` core hypotheses for work at most `2F_C`, independently of the code height and outsider collision depths. If `u>=N`, the completion lower bound can be vacuous; the theorem remains valid. It does not address the regime of a small core surrounded by many outsiders, which motivates the next result.

## 3. Prize-budget pruning with a collision profile

Extend `B` with an unfinished terminal output on every missing-response branch. These added outputs have zero core population and zero core prize mass. In a proper binary code they are unnecessary, but they permit the statement to cover any fixed number of responses. Let `Y` be the set of terminal routing outputs occupied by outsiders, including both core leaves and missing-response exits. For `y in Y`, let `u_y` be its outsider population and put `p_y=u_y/u`; assume `u>0`. Write `w_y` for the core leaf prize if `y` is a core leaf and zero otherwise. Let

    W = sum_{h in C} w_h,
    W_bad = sum_{y in Y} w_y.

Take nonnegative prizes with `W>0`, and choose any rational `eta` satisfying

    W_bad < eta W < W.

Assign each occupied leaf the prize budget

    a_y = w_y + (eta W-W_bad) p_y.                           (4)

These budgets are at least their leaf prizes and sum to `eta W`. On the path to each `y`, choose the first node whose descendant core prize mass is at most `a_y`. Such a node exists by the time the path reaches `y`. Stop at the union of these chosen nodes, discarding any chosen node already below another stopping node. Execute the remainder of `B`.

Every occupied terminal output is below a stopping node, so every surviving core leaf is globally clean and can actually be identified. Choosing a zero-core terminal itself simply keeps the original unfinished exit. The stopped core prize mass is at most `sum_y a_y=eta W`; overlap between chosen cells only reduces this sum. Thus

    completed prize >= (1-eta) W.                           (5)

If `e_y(a)` is the first depth on the path to `y` whose descendant core prize mass is at most `a`, then each outsider routed to `y` gets at most `e_y(a_y)` queries. Core work is at most `F_C`, giving the completely general computable bound

    work <= F_C + sum_y u_y e_y(a_y).                       (6)

This construction is polynomial using rational additions, comparisons, and the explicit code. No entropy computation or approximation is needed to execute it. It is a specific prefix of the directly lifted template, and therefore an exact prefix-pricing routine must return at least its profit.

## 4. Entropy bound for a balanced code

Suppose every child of every node has at most `gamma` times its parent's core **prize mass**, for some `0<gamma<1`. For positive-prize paths, after `t` queries the remaining prize mass is at most `W gamma^t`; zero-prize cells cause no difficulty. Therefore

    e_y(a_y) <= ceil[ln(W/a_y)/ln(1/gamma)].

Since `a_y >= (eta W-W_bad)p_y`, equations (5)-(6) give

    completed prize >= (1-eta)W,
    work <= F_C + u {
         [H_nats(p)+ln(W/(eta W-W_bad))]/ln(1/gamma) + 1
                    }.                                     (7)

Here `H_nats(p)=sum_y p_y ln(1/p_y)`. This proves a collision-entropy bound for an actual executable partial policy. It permits an arbitrarily large outsider population `u`; its route entropy and the contaminated prize mass determine the overhead.

For uniform unit prizes, `W=N` and `W_bad=c`, where `c` counts occupied **core** leaves; missing-response exits contribute zero to this count. The entropy distribution still includes all occupied terminal outputs. If `c<=N/4`, take `eta=1/2`. At least `N/2` core hypotheses finish, with

    work <= F_C+u{[H_nats(p)+ln 4]/ln(1/gamma)+1}.            (8)

For a perfectly balanced binary code (`gamma=1/2`), this is

    work <= F_C+u[H_bits(p)+3],
    work / completed_count
        <= 2 {F_C/N +(u/N)[H_bits(p)+3]}.                    (9)

Using `H_bits(p)<=log2 |Y|` recovers a bound in terms of occupied-terminal-output count. Skewed collision distributions can make (9) much smaller. In particular, if all outsiders follow one code leaf and `N>=4`, their added work is at most `3u` while at least half the core completes, regardless of the original leaf depth. The same conclusion holds for one occupied missing-response exit. A depth-one cut gives a sharper constant on the perfect binary tree, but (7) also handles arbitrary skewed distributions and weighted prizes.

Without a balance or explicit path-mass condition, entropy alone cannot bound the unpruned outsider work: a point-mass outsider distribution has zero entropy and may follow an arbitrarily deep leaf. Equation (6) retains the actual path information for such codes.

## 5. An algorithm-linked sufficient dichotomy

For any requested work price `lambda>=0`, the construction proves the existence of a prefix with profit at least

    (1-eta)W
      - lambda [F_C+sum_y u_y e_y(a_y)].                     (10)

An exact prefix oracle on this lifted template either returns positive profit whenever (10) is positive, or its nonpositive result implies the explicit necessary inequality

    (1-eta)W <= lambda [F_C+sum_y u_y e_y(a_y)].              (11)

One may replace the right side with the entropy bound in (7). For incumbent depth prizes and `lambda=1`, a positive prefix is an executable improvement certificate through the established completion-pricing framework. This is a polynomial certificate-or-lift statement for every supplied code and routing profile. It supplies no universal family of cores/codes for which these inequalities imply a smaller global approximation ratio.

## 6. Verification

`research-general-code-lifting-audit.py` constructs coordinate cores with explicitly routed outsiders. It checks the exact depth-cut profile, the load-threshold theorem, the rational prize-budget construction, and its uniform entropy consequence. Additional ternary instances contain late missing-response exits and verify the extended-terminal formulation. Outsider populations may greatly exceed the core. Small exact prefix enumeration also confirms that the optimal prefix profit dominates each explicitly constructed candidate. These checks audit the claims; no general code-discovery oracle is supplied.
