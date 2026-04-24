# Silkium (INeedANewGuitar) Whitepaper v1.0

**A Decentralized Commerce Protocol**

Author: Evenander Alice (Phan Minh Thiên Hoàng)
Date: 2026-04-24  
Status: Draft / Active Development

---

## Abstract

Silkium is a decentralized commerce protocol designed to enable peer-to-peer exchange of physical goods without relying on a centralized marketplace.

The protocol aims to reduce intermediary fees, mitigate spam and Sybil-based manipulation, limit fake order inflation and review abuse, and remove the need for a single platform to control the entire transaction flow.

Silkium combines cryptographic identity, distributed discovery, relay-based communication, escrow settlement, weight-based ranking, and a minimal dispute model where unresolved conflict is treated as a symmetric economic failure state.

---

## 1. Introduction

Traditional marketplaces introduce a number of structural issues:

- high intermediary fees
- fake accounts used to inflate orders, reviews, and reputation
- centralized ownership of user data
- dispute resolution controlled by a single authority
- unfair competition for small sellers

Silkium is designed to reduce these issues through decentralized architecture, cryptographic verification, escrow, and a reputation model based on weighted behavior rather than raw interaction counts.

The core philosophy of the system is:

```text
Trust no one.
Trust the rules.
```

---

## 2. System Goals

Silkium is built around the following goals:

- no centralized platform with unilateral control
- all transactions verifiable through digital signatures and smart contracts
- product discovery performed through a distributed mechanism
- buyer and seller communication routed through relays to reduce IP exposure
- ranking based on a weight system rather than raw purchase counts
- dispute handling through a simple symmetric rule: Code 3 penalizes both sides equally

---

## 3. System Overview

The protocol is organized into four layers:

1. **Identity Layer** — cryptographic identity based on public/private keypairs  
2. **Network Layer** — P2P, DHT, and relay broadcast  
3. **Commerce Layer** — listing, search, order, escrow, and settlement  
4. **Incentive Layer** — weight, stake, penalties, and treasury allocation  

---

## 4. Identity

Each node in the system maintains two keypairs:

```text
1. Signing Keypair
- private signing key
- public signing key

2. Encryption Keypair
- private decrypt key
- public encrypt key
```

### Meaning

- **private signing key**: used to sign messages and transactions
- **public signing key**: used to verify signatures
- **public encrypt key**: used to encrypt content for the recipient
- **private decrypt key**: used to decrypt received content

The system does not rely on traditional centralized accounts. Instead, identity is bound to keypairs and historical behavior within the network.

---

## 5. Network

The system operates on the following principles:

- fully peer-to-peer
- DHT for discovery
- relay broadcast to reduce IP exposure
- broadcast of listings, requests, and transaction states

### Relay Principle

When a packet is sent:

1. it is encrypted for the intended recipient
2. it is signed by the sender
3. it is wrapped with the public keys needed for verification and decryption
4. it is sent to any node in the network
5. that node relays it onward until it reaches the destination

The purpose is to prevent buyers and sellers from needing to expose their origin IP directly when unnecessary.

---

## 6. Search Engine

Search is decentralized and does not depend on a central server.

Each user runs a local search engine that collects data from:

- DHT tables
- listing broadcasts
- public seller metadata
- local ranking logic on the user’s machine

### Search Objectives

- find products by keyword
- find sellers by region, reputation, or weight
- filter listings according to buyer constraints

---

## 7. Weight System

This section is central to anti-clone, anti-order-farming, and fair ranking.

The system does **not** use raw purchase counts. Instead, it uses a **weight score**.

### 7.1 Idea

A real transaction should not carry the same value as a meaningless or malicious interaction.

Therefore, every account, key, or listing receives a weight that reflects behavior quality, not just quantity.

### 7.2 Weight Components

Assume a seller’s total weight is:

```text
W = Wrep + Wstake + Wage + Wtrade - Wrisk - Wdispute
```

Where:

- `Wrep`: weight from successful transactions
- `Wstake`: weight from locked stake
- `Wage`: weight from key/account age
- `Wtrade`: weight from real trade volume
- `Wrisk`: penalty for malicious behavior
- `Wdispute`: penalty for disputes, Code 3 events, or violations

### 7.3 Proposed Formulas

#### Successful Transaction Weight

Each successful transaction contributes weight:

```text
Wrep += log2(1 + V) × Q
```

Where:

- `V` = transaction value
- `Q` = transaction quality factor

`Q` may be defined as:

```text
Q = 1 - r
```

where `r` is the recent dispute rate of the seller or buyer.

#### Stake Weight

Higher stake produces higher base weight:

```text
Wstake = k1 × sqrt(S)
```

Where:

- `S` = amount of token locked as stake
- `k1` = protocol adjustment factor

A square-root function prevents large capital holders from dominating too easily.

#### Key Age Weight

Older keys receive more base weight:

```text
Wage = k2 × ln(1 + D)
```

Where:

- `D` = number of days the key has existed
- `k2` = protocol adjustment factor

A logarithmic function prevents age from becoming too dominant over time.

#### Risk Penalty

If an account shows harmful behavior, weight is reduced:

```text
Wrisk = a × FraudSignals + b × SpamSignals + c × FailedOrders
```

Where:

- `FraudSignals`: indicators of fraud
- `SpamSignals`: indicators of listing spam or request spam
- `FailedOrders`: orders failed due to the account’s fault

#### Dispute Penalty

```text
Wdispute = d × DisputeCount + e × Code3Count
```

Where:

- `DisputeCount`: number of disputes
- `Code3Count`: number of Code 3 events

### 7.4 Normalization

To make ranking easier, weight may be normalized to the range `0..1000`:

```text
Wnorm = 1000 × (W - Wmin) / (Wmax - Wmin)
```

If insufficient data exists, the protocol may default to `W = 0` or `W = base_weight`.

---

## 8. Transaction Model

Each transaction contains the following basic fields:

```text
- transaction_id
- buyer pubkey
- seller pubkey
- item_id
- price
- timestamp
- status_code
- signatures
```

### Principles

- every state transition must leave a verifiable trace
- all critical data must be signed
- smart contracts are the final settlement authority

---

## 9. Listing Model

A seller creates a listing containing:

```text
- item
- price
- description
- region
- public key
- timestamp
- listing signature
```

The listing is signed by the seller’s private signing key and broadcast to the network.

Local search engines read this data from the DHT or broadcast stream and include it in their result set.

---

## 10. Buyer Flow

### Step 1: Find a Seller

The buyer searches for the desired item using the local search engine.

The search engine uses:

```text
- DHT table
- listing broadcast
- ranking by weight
- region / price / description filters
```

The result is a set of matching sellers.

### Step 2: Send Purchase Request Through Relay Broadcast

The buyer creates a packet containing:

```text
{
  item to purchase,
  delivery destination,
  timestamp
}
```

Then:

1. encrypt the packet using the seller’s public encryption key
2. sign the ciphertext with the buyer’s private signing key
3. attach:
   - buyer public signing key
   - buyer public encryption key
4. send the packet to any node in the network

That node relays the packet through the P2P network until it reaches the seller.

The goal is to reduce direct exposure of the buyer’s IP address.

### Step 3: Seller Response

The seller receives the packet, decrypts it, verifies the signature, and sends a response packet:

```text
{
  item,
  delivery location,
  delivery time,
  additional description,
  timestamp
}
```

The response packet:

- is encrypted with the buyer’s public key
- is signed by the seller
- is relayed back through the network

### Step 4: Buyer Funds Escrow

The buyer sends funds into a smart contract on an Ethereum/EVM chain.

```text
status = FUNDED
```

At this point, the funds belong neither to the seller nor to the buyer. They remain in escrow.

### Step 5: Transaction Confirmation

The buyer and seller sign a shared message:

```text
{
  item,
  transaction_id,
  signed_time,
  code
}
```

Where `code` is the final settlement state:

- `1` → successful completion
- `2` → return / refund
- `3` → hard dispute / unresolved failure

This message may be written on-chain or broadcast for contract consumption.

---

## 11. Seller Flow

### Step 1: Create Listing

The seller creates a listing, signs it, and broadcasts it.

### Step 2: Receive Request

The seller receives a relay packet from the buyer.

The seller:

- verifies the buyer’s signature
- decrypts the content
- checks format validity
- verifies item legitimacy

### Step 3: Respond to Buyer

The seller sends a signed and encrypted response packet back to the buyer.

### Step 4: Wait for Escrow

If the funds are confirmed in the contract:

```text
→ prepare for shipment
```

### Step 5: Ship the Item

The seller ships the item to the agreed destination.

---

## 12. State Machine

The transaction lifecycle may be described as:

```text
CREATED
→ REQUEST_SENT
→ LISTING_CONFIRMED
→ FUNDED
→ SHIPPED
→ DELIVERED
→ SETTLED
```

Alternative branches:

```text
FUNDED
→ CODE_2_REFUND
→ REFUNDED
```

or:

```text
FUNDED
→ CODE_3_DISPUTE
→ PENALIZED
```

---

## 13. Code-Based Settlement

### Code = 1

```text
buyer + seller sign code 1
→ smart contract releases funds to seller
→ transaction ends
```

This is the best-case state.

### Code = 2

```text
buyer + seller sign code 2
→ refund buyer
→ full or partial refund depending on policy
```

This is used when both sides agree to cancel or return the transaction.

### Code = 3

```text
buyer signs code 3
→ hard dispute
→ no objective fault determination
→ both buyer and seller are penalized equally
→ penalty funds are transferred to the community fund
```

#### Why this design exists

- no verifier is required to judge who is right or wrong
- no complex evidence system is required
- dispute costs remain high
- Code 3 becomes expensive to trigger
- spam disputes are discouraged

#### Nature of Code 3

Code 3 is not a refund state.

It is a **symmetric loss state**.

If a transaction reaches Code 3, the system treats it as a failure state in which both parties share responsibility.

---

## 14. Penalty Formula for Code 3

Let:

```text
P = item value
```

The protocol may define:

```text
buyer_penalty = α × P
seller_penalty = α × P
```

Where:

```text
0 < α ≤ 1
```

For a strict configuration, the protocol may set:

```text
α = 1
```

In this case, both buyer and seller lose 100% of the collateral locked for that transaction.

### Penalty Destination

The penalty is not burned.

It is transferred to a **community fund** or **public treasury** of the protocol.

The purpose of the treasury is:

- audit funding
- bug bounty funding
- infrastructure support
- community operations
- transparent public accounting

---

## 15. Why the Penalty Is Symmetric

A symmetric penalty is the cleanest choice if the protocol wants to preserve the principle:

```text
Do not judge who is right.
```

If the penalty is asymmetric, the protocol implicitly assumes that one party is more trustworthy than the other. That shifts the system toward adjudication instead of rule enforcement.

Therefore:

- buyer and seller accept the same rule set
- severe transaction failure results in equal consequences
- no fixed institutional bias is introduced

---

## 16. Community Fund

The community fund receives all penalties from Code 3.

### Fund Objectives

- pay for smart contract audits
- reward network operators
- support developers
- fund scholarships, community work, or socially useful projects if governance approves

### Fund Principles

The fund must be:

- public
- on-chain or otherwise transparently recorded
- easy to audit
- independent of any single individual

---

## 17. Verifier

In the current design, **Code 3 does not require a verifier to decide right or wrong**.

However, verifiers may still exist in the protocol for other tasks such as:

- checking transaction format validity
- confirming that a broadcast packet follows protocol rules
- participating in other future system modules

### If Verifiers Are Used

- selected randomly from a staked pool
- multiple verifiers may be used simultaneously
- misbehavior is slashable

But for **Code 3**, no adjudication is required by default.

---

## 18. Stake System

To participate in high-responsibility protocol roles, a node must lock tokens into a smart contract.

### Stake Purpose

- increase trustworthiness
- prevent spam
- raise the cost of malicious behavior
- create economic accountability

---

## 19. Slashing

If a staked role acts incorrectly, its stake may be slashed.

Examples include:

- validating incorrect data
- intentionally disrupting the process
- committing fraud under the protocol rules

Slashed stake may be used to:

- reward the harmed party
- transfer to the community fund
- support protocol operations

---

## 20. Common Cases

### Case 1: Buyer Disappears

If the buyer fails to respond within the allowed time:

- the protocol uses timeout logic
- the current state determines the outcome
- assets are handled according to predefined rules

### Case 2: Seller Fails to Ship

If the seller fails to fulfill the obligation after valid funding:

- the transaction may move to Code 3 or a timeout failure state
- penalties are applied according to protocol rules

### Case 3: Buyer Claims Non-Delivery

In this design, Code 3 is not meant for lengthy argument.

It is a hard failure state with symmetric penalties.

### Case 4: Dispute Spam

If a key repeatedly triggers Code 3:

- dispute score increases
- weight decreases
- participation fees may increase
- the party’s listings are ranked lower

---

## 21. Threat Model

The protocol must resist the following attacks:

- clone accounts used to inflate orders
- listing spam
- relay spam
- reputation washing
- fake packet injection
- repeated dispute abuse

### Mitigations

- use weight instead of raw counts
- require stake to increase attack cost
- use digital signatures to block impersonation
- use DHT and relay routing to reduce dependence on central infrastructure

---

## 22. Core Principle

The core of INeedANewGuitar / Silkium is:

```text
Do not trust people.
Trust the rules.
```

The system does not attempt to decide who is good or bad.

It only defines clear consequences:

- successful transactions move funds correctly
- valid cancellations return funds correctly
- Code 3 forces both sides to bear an equal penalty

---

## 23. Conclusion

Silkium is a decentralized marketplace protocol with three central properties:

1. **Distributed power** — no central marketplace controls the entire transaction flow  
2. **Distributed discovery** — search is driven by DHT and broadcast  
3. **Distributed trust** — settlement relies on signatures, escrow, stake, and rule-based enforcement  

The ultimate goal is to build a system in which:

- transactions are verifiable
- fraud becomes expensive
- disputes become costly
- the community benefits from maintaining the protocol

```text
In this system,
you may fake emotions,
but you cannot fake signatures,
you cannot fake contract state,
and you cannot fake the consequences of Code 3.
```

Acknowledgements

This protocol is shaped through iterative feedback from developers and the open-source community.

