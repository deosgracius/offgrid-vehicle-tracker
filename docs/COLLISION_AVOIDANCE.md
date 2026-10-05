# Collision Avoidance and Frequency Interference

The professor's edge case: both radios power on at the same instant, both want to
announce themselves (NodeInfo) and establish communication at the same time, on the
same frequency, with no coordinator. Who talks first, and why doesn't the channel
"crash"?

## The short answer

Nobody is assigned to talk first. LoRa is half duplex and the channel is shared, so
Meshtastic uses the same philosophy as classic Ethernet and ALOHA: **do not try to
prevent every collision — make collisions cheap, detectable, and non-repeating.**
Three mechanisms stack to do that, plus one physics effect that softens the worst case.

## Mechanism 1: Listen before talk (CSMA/CA)

Before transmitting, a node asks the SX1262 to perform **Channel Activity Detection
(CAD)**: the radio listens for a few symbol times for the signature of a LoRa preamble
on the slot. If the channel is busy, the node does not transmit; it waits and retries.
So in the common case the "collision" never happens: whichever radio keys up even a
few milliseconds earlier wins the channel, and the other one hears the preamble and
defers. This answers "which one talks first": the first one to start transmitting, by
however small a margin — and if the margin is big enough to detect (more than a CAD
window), there is no collision at all.

## Mechanism 2: Random backoff breaks the tie

The true edge case is both radios passing CAD at the same instant (both heard a clear
channel because neither had started yet) and transmitting simultaneously. The packets
overlap at both receivers and, in the worst case, both are lost. Nothing crashes: a
LoRa collision is just two packets that fail their CRC. The cure is that every
transmission is scheduled with a **random delay drawn from a contention window**, and
every retry draws a new random delay. Two nodes that collided once will almost
certainly draw different delays the next time, so the repeat-collision probability
collapses geometrically: if the window holds N slots, a second collision has
probability 1/N, a third 1/N², and so on. Determinism is what would be dangerous here
(two identical radios booted together would collide forever on a fixed schedule);
randomness is the feature.

## Mechanism 3: Nothing important is sent only once

The protocol is built so a lost packet never strands the system:

- **Directed packets** (position requests, direct messages) are **acknowledged**; no
  ACK within the timeout means the sender retransmits, with fresh random backoff each
  attempt.
- **Broadcasts** (NodeInfo, position, telemetry) are not acknowledged but are
  **periodic**: NodeInfo goes out on boot and on schedule, positions every 10–60 s,
  telemetry every 300 s. A collided NodeInfo at boot costs at most one cycle of
  patience; the next one gets through. This is robustness by repetition, and it is why
  the simultaneous-boot case heals itself within seconds even if the very first
  exchange is lost.

## The physics bonus: capture effect

LoRa receivers exhibit **capture**: if two overlapping transmissions differ by roughly
6 dB or more at the receiver, the stronger one demodulates correctly and only the
weaker one is lost. In a two-vehicle system the geometry is almost never symmetric, so
many theoretical collisions still deliver one packet. Chirp spread spectrum also makes
same-channel interference look like uncorrelated noise after de-chirping unless the
interferer is another LoRa signal with the same SF and bandwidth, which narrows the
set of signals that can collide destructively at all.

## Walking the professor's exact scenario

1. t = 0: both radios boot, both prepare NodeInfo.
2. Both draw a random tx delay from the contention window — already they are unlikely
   to be simultaneous.
3. Each runs CAD before transmitting. If radio A started first, radio B detects A's
   preamble and defers; B transmits after A finishes. No collision, "first" was decided
   by the random draw.
4. Worst case: both pass CAD in the same symbol window and transmit together; both
   packets may be lost (unless capture saves the stronger). Neither radio crashes —
   each simply never hears a response.
5. Each reschedules with a new independent random delay. The chance they collide again
   shrinks multiplicatively each round.
6. Even if several NodeInfos in a row were lost, the periodic rebroadcast guarantees
   discovery within one broadcast cycle. In our bench experience, two radios
   power-cycled together appear in each other's node lists within about a minute.

## Frequency interference more broadly (the 902–928 MHz reality)

The band is license-free and shared. What can interfere on our slot, and what happens:

| Source | Effect | Mitigation already in the design |
|---|---|---|
| Another Meshtastic group, same slot (same channel name) | Real LoRa collisions; their packets are undecodable noise to us (different AES key) but still occupy airtime | CSMA defers to any LoRa preamble; our low duty cycle (≈6 %) leaves room; worst case, rename the channel → new slot (Idea 2) |
| The public mesh (LongFast) | None in-band: slot 19 = 906.875 MHz, 6 MHz away | Private channel name = private slot, by construction |
| Non-LoRa ISM devices (older cordless gear, LoRaWAN uplinks hopping across the band) | Raise the noise floor momentarily; SNR margin absorbs it; a strong burst costs one packet | 23.5 dB measured SNR margin at close range; retransmission and periodic rebroadcast |
| Our own two nodes (the professor's case) | Rare first-cycle collision | CSMA + random backoff + capture + periodicity, as above |

How to demonstrate this for a grade: with both radios on the bench, power-cycle them
together ten times and log time-to-mutual-discovery from the OLED node lists (expect
well under a minute each time); and watch channel utilization during a busy exchange
to show the airtime discipline holding (we measured 5–6 % idle with CLIENT_MUTE).

## References

- Meshtastic documentation, "Mesh Broadcast Algorithm" (CSMA, contention window,
  SNR-weighted rebroadcast delays, hop management). meshtastic.org/docs
- Semtech, SX1261/2 datasheet rev 2.2, Channel Activity Detection (CAD).
- Semtech AN1200.22, "LoRa Modulation Basics" (capture effect, co-channel rejection).
