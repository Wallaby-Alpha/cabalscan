"""Shared config for CabalScan — imported by both app.py and scanner.py."""

# Place your target tracker wallet addresses here (up to 230+)
PRESET_WALLETS = [
    "5N69dUvxdiQGFaRob32oPSwLuUYTqNgHz6GoEtnrRd8S",  # suppoman
    "AQ8t7FmGaDQ4AqmNtaX2d9NqfACCHb16yKo8BavExWkV",  # suppo1
    "2UGhBWG6K9UJq5iM96t1PebJfCBuNxYgYjwNsvE9nwBw",  # Suppoman alt5
    "8qRh4cJDH9bBAgUHHuoudBMoDsNHsrjDVHsAd3PXxZ5A",  # Suppo alt4
    "8H86inoTa6PfeoCgRiuup2ZFkeR6WMQYTJWNtHcdSpQW",  # suppo?
    "Bfujsb5We6iW4JVTocFnHcCuH2NZawAaawawdsSy2G2N",  # crypto gains 3
    "ADiP2QxRegS56oP9bEbnVm3Kv9Si8d931W75DWRQiU1Z",  # crypto gains 2
    "FKjyLNBEaio8TMRT4R5KvAm6viYHYLXPogZVsV23kmzc",  # crypto zach public
    "6vPb1fgadFCnmjHHHb8wVVYXXRyv66ZVHBwS8KduVtDD",  # crypto zach confirmed side
    "CWscK3ppFqXR9auTLxkwwLf31DP6KuZ1BqKE6UpvWbTv",  # Crypto Zach tucker/cbm
    "AgbYtSqB2LEaP6BzBwsQ8eRp7bMRwqJz54DEzYdkmk5v",  # Suppo Sol 2
    "3pSbsfviHu1ERTKMpfzPNbHA75ffvx37h7uyvBr2tamd",  # Suppo Sol 3
    "F6zTiTZo9Gx3gSXzWgRot7kqWxMdsAmhYCfk5qKuXVZL",  # Kyle Doops
    "BkCQ9T6HeGZmuHRpF55dJ47TU1bdSUcf5dUVRP5jdqrN",  # Suppo New 1
    "ErSwAVyTNxbLxwERXCeHJECeehhEdZtVSSMJxsKoigon",  # suppo/cg?
    "HFozUwnbKHE4quZZcQiYShkmQ2kZvJayNvxBNQoAo7hY",  # cg?
    "Gjae1mkaRxbAgsEwSYfwvJneH6sfz1mCoAznmXV4iRCd",  # cg robots
    "8udujy8heeEYnoeN4H3pY2EAED2ZsfAn8uWVtqgAJQBR",  # antisniper
    "H9C5wWzkm72atwk7Gom3tns1hnMYt28iKmUUVMrgZgp7",  # sindoor
    "HwzHpQCGS1fJbF3YFyWVcAjR5kuZW79bDusoj4SH7C3k",  # new 2 suppo
    "DdgY42vCyJkuhFVwH4SAZBmoUKxPY7q7qyUubvdkd7RQ",  # new 3 suppo
    "J3ekaUh3CM7SNVAoyGncKg9s86JffFenLJqWNEn1cjx9",  # Follower
    "2XkjbK82TEf9azFaSiVkRKRn5x3XbMQaydUF4fahPvuG",  # suppo bully1
    "66N8cLukCYD8XTb6HxZpYKKEv7psa6rjHt3fRtj2dvxh",  # suppo bully2
    "5NDGWY5ahREkWsiUZhod5XQHZUkqFAcnebTkkDXxy1Ng",  # Rubicon
    "FSF8wftBC6yX6dRhruqaeQBMLhKqKF2rUbNq3dyBqcVP",  # CG new 1
    "72EQ7KLyLGxubJCcBrqjjRzqVuv69WgT7Riy9E9cvfhX",  # cg/suppo new 2
    "HMWoXFdicDDLpj8oWG4WGx51gaA4rses6DXWwwRa68dB",  # Suppo Bully 4
    "Y9GWjAt5XCwA4RM5usG5Ymyvziy8gRFci9aX6V252M1",   # Suppoman tracke
    "BKKJtyzpE5He7uDtqcFgaXh5UZ6tZ14ZjRVaaJQrs7ho",  # CRYPTO GAINS
    "aQdDcJ3DnZe9DNT5rk7gJqiz4NF3LrPtLMYqQgJAPaj",   # cg squirrel 2
    "WJpRJzVvMfCSv4bzZLZCBd719ufvgLCR76Wkxjr33e9",   # cg squirrel 3
    "8oETpd62mEr9bYJ8dGDRDtv4wc3DeSwybd2E23is4jJy",  # cg squirrel 4
    "DTpekwcCuPDTWm5es2W2mZax33rYnzwHWCAq6zV8KDgh",  # cg squirrel 5
    "GBZmnPzxcMnZkdHzHYnAc6b8ocT9K4ZHecJi8UZ1J1Wj",  # cg vbucks1
    "E8JkqZ4BBEGWc6SmHQX2j8kn5GYu3WjxSPRqpmBkB4uG",  # suppo ninja1
    "CsAdVm9AxsvuzMyXCEfX2VKNiFcHacg7Fxie2WCRqUhr",  # suppo ninja 2
    "7nXLN8rh2UMtzMHPqRBun6ncfK3GjvZwSkm3zLPPEXNV",  # suppo ninja 3
    "F4FMGhL6SJaZZP9fmCxiUqUz2CSABEHdj9ABrXQbTgeb",  # suppo ninja 4
    "Fj33PrX4LCwqTRpLHGccqHid1qvdeUxbwkoRTFSfUyjU",  # suppo ninja 5
    "4sYgCsFmxnZhNrfJ4xihMU9Q52Fpj3wzWPknUXkSKtHr",  # suppo mortgage1
    "DGJvKGNmGszfnYzv3WdgB6chT8NdiUZQxARsMUtQAAND",  # suppo connect
    "jTreizFAcJTzAQGjLibVqa7BJYyyXRqtBhXJGywEVEP",   # suppo mortgage 3
    "CEvuhW2QnMbdweLPkooiGZDYmBz2Akxx7o4uLZ3PEQhk",  # suppo mortgage 4
    "DYrMUyszqtKBszKdhrVR35X5b2tFKKX7y8TrGy5ZaDxc",  # suppo PORT
    "5inVmnvCxeBtBPACEkLpS2hgx6Hi9JL8G22Sfz2iZHYP",  # suppo MEGA
    "7D8jMyRHeqULXWnmNXisfqaPJLYHaYin5Y2LiZn4A9nr",  # Suppo MAJOR
    "14FfkJpAjraKnPZdZCczgSMbw1mUbr5XrJMNEu6aKzvG",  # cg? suppo?
    "46fHjStWyKonc7QrtD1kQLYavGk3iLu9k4VAF67cwwcG",  # nin1
    "2yFn8jn9PcBPqrpqKEMby9QkGvy6hpBoQ3Dw4qitJHfN",  # Suppo HFN
    "EZ1iuVDEJbNhKvp4PxnTmtrrfNFF8ELW53eSVNweFJ31",  # nin3
    "A9KWS4Cbn7xeDBdnmcVgz3u63vtcYLXYNr8DB4oXtXkw",  # nin4
    "FMhQ7KCuKoDNiKHBi3fSKLYcGTdf9iFsADoAjhHhQHCn",  # SupHCN cnct-and
    "GhDvDWzw1rZuXLqrmKvavC2XyFS76YjEsj1hyjHszvdp",  # b2
    "41bhtRrQ6QvSespWWEaTCeahguYaq4YSUofaH26Qo3KT",  # b3
    "86jTb3yxGXEYYEjboYWcTY8xwqfTfz84Sbvt8ZP4scTq",  # b5
    "AVEdK2oG88tabPNGYSbJW41zMSsjadp6ZkqnBYxXp7Rm",  # pk
    "G64VpM645W8iUMQuzq8J5rTV4McePSpVtQj7Gzw8t5Hq",  # Suppo Port CONNECTED
    "EnLr63K6KvAp34kQP42PfRU6PcLyPKYoXPFzmWzsWiEY",  # Suppo connected
    "FLRJFaxkKBtsuN5nQTKqQ7TxSByV1brzabt3Fmbvrz5w",  # spom ninja
    "mfguNrfhLiEkMUMSWmb54DT64PmT3rMvyEVFi9S7gyH",   # spom ninja 2
    "DnB1DLTeS5rqAkmFmH5rpS8sVVFSu5ircjKdc7aeeNCM",  # Spom Ninja 3
    "C6Gj8u3pXAXte3LyvAgAE7s4KKdHQXXRC4ZFMZJCtm6M",  # Suppo Giga?
    "HkS3GXY1AU97xuLBie6VWgTefw1i7nmLSr2CcmWSZsGV",  # suppo - cnct to port
    "4orogPNfVbPgyN8oKoHSiGKfnuworVFavoQGdp2YpVoP",  # CG Trash Memes
    "4L8d5uFZrkFdNd6q1Si8joXmx1U6aUkMnVUeSpbivTRC",  # CG c:memes 1
    "FDiSLdiKrgZPBiZN4QaG883UFzvQQnYUSZmsYJh2bThT",  # CG c:memes 2
    "AQmaqp5RpLXDJSRAxJKL13WiWkAgXMLwh4s6EovS7aLJ",  # CG trash - memes
    "CmJ6gGVP4q8FeFtqs5D15W4AyxUiveTqVdMavUNEgw1J",  # CG!!!!trashmeme
    "4VzMg7B2bCNqaRvrqC5aCPRYPXbu7zVxyAuyj8Kp3bJS",  # HMO Spom
    "8KF7RtTYugwLrEWtZwC6HZXyZrmAhoLzx7jkdtWuerBg",  # Suppo HMO 2
    "FCMh9rhCzF8wkMc2fe9DScyFBD39PTMyRE3Pa1zkzJHy",  # CG Lol/Seekai
    "GAMx7B9TY5jKKseZDE1hUmPSoo9d4dKWJ9g6LDoVFz2J",  # Suppo Negan 1
    "8HBhhEQH2iDW3roy5koBH2sjwAgRxKSaZwvNhvFAJadM",  # suppo giga?
    "A95p4sED3VBXJepXS7VjQsAKeHfRWecWuZePMKmT8mta",  # Maybe Suppo?
    "5rzrYVvREQjfJZ4NNb3cbsBTmFiiE2GeGs8VcW8paa6y",  # Telegram AndyB
    "6FD5FijB93BxarebSjDcNeRCZK8vf1rMtEKY9qeW1DEr",  # Telegram Group2
    "G6C1DxMSJ57CEcYtQiwTJRv4eFYbW47b615waZLB4fUZ",  # giga dev1
    "GxYTZvdrTeHBYvjE6dLQke5RtsBLX4knyvuXwbTC71bM",  # negan2
    "DJJmT3FBqjivxZd2kasgYDHxNVmsheqWhtj2d6JpVcnf",  # negan3
    "B2f9ubz5ztzeNtzqwrg9YZ68A2n6Vvpf32gzUXPF71Kq",  # negan4
    "BgzpfCwKKsDFdENcgbse8CTEHgU5eBqK7Zvb9RsYrcPL",  # telegram group5
    "HPt5nDNpf99Hi4XARXYNGKMyT9oBymgJ8f8Fqyi4hcmN",  # CG Retail Guy
    "A77ZErL8ebYLGiTrY1XyHoaHhjkxTfnSfm6ENnCbnAJf",  # CG Retail3
    "DGuZnBKdpJNVhMAaKpEv2wB7deqjtbVN8FtzdL3yHAc4",  # Telegram Droz
    "CJRLAWHoG6p7gcoY4m15G3ZFiJje7btwXkcbf7nDdE6s",  # Telegram 10xHntr
    "8urHCg3RBqWF7LQSk2rbTe4EWh3dhYPLGZ8WnEbuEviL",  # Telegram group3
    "8oJJuG5MLXBLSfwCMELzkUNrAiTPaTFqgsFDmqck3Fmf",  # Telegram Group4
    "DQ9xct3btLPaCrnSgQW7o9iS7SHzGLxTJgsZ6dqS4Bmr",  # Suppo f925 buy
    "5SHc1ymh5fEYzmHydxQCHiUxYPHSZRk2KfqNkfuokPhr",  # Suppo follower
    "9vbt8SNdWwB8cEWkyZDrpVXAQMwkuFLCTNB3R8nrXNLC",  # Win All Day?
    "FXzLRnzn9knVK8zTNGxenDHstTkVGzCR1kKDfBDaJVKV",  # CULT trash
    "4bRiZ2p4eRWpVWV8yGU588K3JSTdfzGjKTzJfSQdd2RL",  # CULT trash2
    "GKHVpw8umdML7d4NqQetcPPbZqaZ7sbzSVsw7yD2q3Y4",  # CULT trash3
    "C9Q75kpAP9NnEwsjmYhRX72Z2FLiSr3kZPxkr1E8k19m",  # CULT trash4
    "83inDF9iH167knFh54S1ZBse2EcyMo5rcEZUxCUSSVvU",  # CULT trash5
    "FMwFDEJ7wGTzGBWvscjyxJgMUpFpEEoLWiMwtHcfUo8A",  # Suppo Tits
    "9asvyWEWKcyTiG9tYAneiSbi3S2BUfJCmK9gWRaJGYwk",  # Suppo Feet1
    "HHBHjy3S1fp3f3vccB4iYUBF1Lwp7vdaPfLfY3ni8ykH",  # Suppo Feet2
    "7qKxCiZQ7ZG1Ct8yk7nDVRLghNz3jNRpw1TjRJhK7Bcn",  # CG Bread Memes
    "HBZtiaiFfQHMJGn5bWfAS3Qn3ufkBSjm2esrkY2LT8Sg",  # CG bread memes
    "6R9noJaCdnJN54HyMm7yLJyiung7xRJ1PQFsw7JrrF7i",  # TG Group - WIM
    "5C6LHDSfwM8FjVuyDhQTtzhAeWGRoxssjdRuZeAeLQsp",  # Suppo Marie?
    "A4grzCdRYWbuzLeUqTp5Hhn1GZHaGoVXqNV7ZDqQpA7W",  # telegram group5
    "89AUSZhkMaXB38P2Zobi4ozT8yBUVChyvRLUv5TdDUH8",  # CG - coinbit
    "7ZnbGnu5mt1Br41Fzu8ikwFVXuSozBv3YC1AJN3GSf5n",  # suppo connected to hfn
    "NnQzYEt2p7otFGcoKDehAbycrMdJnMXoP5x2Rp5gTNp",   # grandowge
    "FLtQBx63VVK4p4mXePKeWBN2HVRiHBtaW2KgT8ekFd4c",  # connct -AAND
    "GEphCQRSdVBq9MvLssZso198d2sTgSXxZsiiHmjPVdx4",  # guy who follows
    "5Koxy8TDLjMGzuP9qFpo7BfpuKe5WqfHDfNzHRE11NRt",  # connct to -hfn
    "6icj6RCZmL3BbSDE56bhqNcgmpyNfw2TEJJLSktvEBEh",  # sup conct to f925 buy
    "6JHaZaHHL49SDfks87xbeosMrcrBEfEockyJHZjzqK9k",  # test
    "DqAXLmRTR5RCU5UTTLXxvfiAh9KjK4DtjRcpsJDeiJYt",  # ustream gd
    "9NRrppLN1XMSqmLgN61fZtuEaagLSGSM91gcxVdjNVHM",  # ustream gd2
    "12VGCoTPz6oecXD9y2zMN3BZyqdg2d7kTAJRsxAm7UBH",  # Pump Fun
    "AmHX3tvgjsosdUXdH9J3q2R4vncMFbHgPS2a3rkZ67eS",  # Land Giga 1
    "FxkYAJLtBoCSYeRRc6hCKrGhgu2cd7MqL3aTdWCUnYbN",  # Land Giga 2
    "AR85bDQGKkKxVhdNWfLWm2HrPs5ZYbYzWmod6MwN1ECj",  # Telegram Group4
    "7NysB6n8qsUx2PAUSjLoWQFjRgCV1rpog5xPhYpo1zHc",  # Marie Creator
    "8s7aNM9nD9GXYEqeZZykK5a2S2Q7AeJ4Wxg6svxPhpGi",  # cnct to Marie
    "AaZkwhkiDStDcgrU37XAj9fpNLrD8Erz5PNkdm4k5hjy",  # test
    "6HMoJqFfifATfSqD7YY3YXA3CZxwjfCwpExGEvQ5bekY",  # alphastrike.sol
    "2bu3tNi1NfDvyG6RMGPUWYiUvgsFKdKvAiN1tXtyCUxX",  # fried
    "EqYGemqo1DeFkKoAvps8baQNqaLEHaTg1EBkXTxa431",   # Altcoin Gordon2
    "A8L7hRc3qUbA9JXb4D4NcYtECx9qzpY7KCoz6kAwqqx5",  # Altcoin Gordon1
    "AxebAp8y2WeBePpwXHbgDo7RqNFbHjtEABqemKbBZ8tc",  # cnct to negan2
    "5SvEcbKh32Yk3TpuWXRUoxKuujX8zfKVUarPXRESqtvd",  # cnct to -wiey
    "5vV7ckkxofwmz1xSRn3F18bcY62HoZzFhcgMFpD71aLu",  # bitty buyer
    "teStzXQ6CwnVkhzzSxskjFJUUzsGuzokuYCf9w5Sjxt",   # Bitty Buyer Connect
    "HtMgPgsjokdspHk6guFXHaayvrqXn288PUsK9CnfjPXM",  # TG Group 6
    "DfLKQ6j1ZniwibSysRs7yaZ5fi98MRN1nMyzNcxzo9uU",  # CG gigadad
    "EkDzy9WXV3pKYwTVKCW3zTq5hhwvyAnQMjikSXE5RFzo",  # Guy in Suppo gr
    "2j5icyy6o9NcNjxYGxUPveAX64ygyXxYN7bJmP7JwT52",  # Suppo follower
    "EA42u6qrpkWgBDACRLtQy2JAax5ZfPoYxpTNYg3vbFaS",  # CG E-T-H 2
    "GDTxj3ZirX1ejrt8zqgioh6CaKEn8siA8ZpVSH4NpeYW",  # CG - MMIP1
    "7MwSR5Y3V9tCxTAgAWfL3kwu2LziKbhkE6z4WewyXvig",  # Fresh Giga1
    "sm2TmB17kAvHb8R2qaWYNSfQYRifGKaDQ4Yn5UyXsEj",   # pk2
    "CnpPPRy87DthsPDDSAeGGuQhPEJx6j2HCRPR2fYZLuG2",  # Fresh Giga2
    "6uBKte2HfwCddSAZmS86ePzCg1zNEohYx6U95rgMS5FD",  # cnct to SuppoTG
    "9hLiEFhLFSotsbZnYt6GHttHUiX2VRM1UXH2FfuDBps2",  # CG Bitty
    "2K5iaXtq6XsUspRtYkfkVAuyVM21STdTUbZBmBJH1DKs",  # CG MMIP
    "5CvCsDJUeFoLGhhjhHZDAxnkcrMuUKAbZFQUkQ6aj24E",  # CG MMIP2
    "FQWYMzji9WLaPEiuSoEd9AFS7CStXZew3ha6NcSbRBbu",  # CG MMIP3
    "5N2DB6b7zZEqUMNhyxcys9afARn7L3tH2QUP12i1fPwa",  # CG Giga
    "B3Qz21iaybax11XgQrDtNmuG8U6QpPXB57sgtxE4Wpbh",  # Suppo honey
    "J9oCqq3nbGoNPAX4TX7US54vhPkz7ggyaktaDi85nbLs",  # CG DOX1
    "VEUPkbAd2oBcyBU5ucRda9u9sEJrRxZzkNi9ksHGJTG",   # CG Dox2
    "EjpE7E5586RcbiaPoJeXG7cLPWYFhJkyCY9SL3m49cgf",  # CG Dox3
    "EpuMRmBj5jmqnr2Zx1TDUuozMDuMyAQiD4VP6TM7miLv",  # CG Dox4
    "CKUhxNE9eWDsm5w9otjXZFVLkUcwjtGnjmyXjSTdQZR1",  # CG Dox5
    "AHUvNNWjzyvGdT4pc3dheAGK42ifUWZcKscR6YqAd9i6",  # CG Dox6
    "14Na35u5xdAywXGrLrmqAJ412V46588gLKc4rtBGNozJ",  # CG Dox7
    "CrHb8bz2x4f24FBAqr9mKM3J6iqCwqxcaLTRStefsQmV",  # CG VNTR
    "v5r7d85xnQ9nk7aMm75cD6NM29tm1jWsp2r5sznQosS",   # CG Dox8
    "915qNoGNtZGMmTBPteXinmDk2hmot921H5tQK2RWwC4x",  # CG Mudeng
    "4Z1NjgKje6Pwb5QdmdnHJENiYujmWjawzKfm872YX6PF",  # CG Dox9
    "CfkU8TohFjF7zM5QPffFGphxEfJyj2mn1KL3CvKNu7cq",  # Suppotrsh giga
    "CLdA3RBUcAAzEXXZcMYpqHFkxrZ25cyMStXJ5G3FUWW4",  # Telegram 8
    "7Aru8gbneZZDhEhnSxmexePyTUDSTvLFYpUxh3Rn2xa1",  # cg RETAIL
    "7stVAuYoj69rU4GERTpt1t5MLzAJ6bmbrihngrKXkw3t",  # Suppo Boat
    "BjTpQ7ktUFtsf7nhxjZ5ncfNJM1WTkapw7Ycupu2URrd",  # CG tremp?
    "Eb4HpAMtqVprLMtchgyWLZ93e3FE35gNXJbC7FNCWcbv",  # CG DOX cnct1
    "65QnhwsD7myZBkCgdCCPKQGE5auNYAMB3pJt7KagiNbW",  # Suppo honey3
    "HWHFvqfBGubwZttu5uKSSDEoh25nvRcVEysCZh6vLUdx",  # cgdx 1
    "CiRRp8ykLmuYjy4XijfV6YwYdSMKNs26C6Huz5UedRqw",  # cgdx 2
    "HazKSo6DK95mvdRwLmU6GiQ8N1TZwixfguyMLgYDDJGL",  # cgdx3
    "9Fa5VKhvhYC7smExnPR2i1gtQnhk2xqA8Jvw15TwFknA",  # cgdx 4
    "6MxfbUeLEZPVxwMXztrzZKdyKkvNjp1eg46gVF3TB5jq",  # cgdx 5
    "QpXtSwiVWtwL4VF69doEZqNNn4Gt1QsovLrVgBQsKZw",   # cgdx 7
    "3rbdpAbmFWVwZaWnCNGBwdUB8WppoQDTsvkUTw3NTpnh",  # cgdx 8
    "6qWUokEUNc9Tcpn43viUyt41BarU47BtRqDSHmw8Znzu",  # Suppo Potcoin
    "863eTpU4DTTqnrXQTsy1mUGzXopbH1SHLpEr45aL1Jnm",  # Suppo Kitteh
    "EnR9oKxVgNtL2DR9S9U6LtcJyBGUd2TVtYsfia3dX3S3",  # TG group Andy?
    "Bejd2UmNi29c4amjJJaKTCDoFU8Uoqgp5CyB1YYCafRD",  # Chrome Axiom
    "3QWnrGBQHpEjzYrKR2T2GEFWGAsp4N2JgEw8MfNwBi6e",  # TG group
    "8Pe2vwFAZM8HRej5C5sXDmZon5FEeQgsJGsESAojkrna",  # trust
    "2n5jXt9YwL4VDaarUVpeFzrAxhQKm8PrfJywGxaFciha",  # giga awr
    "HdW58hqd8UmYZeuwEwHXmP9ibAuazfbYbtsP5XWfa6pc",  # giga sol
    "7EBEdGXKEg4za5ZcvaNM4obYJAqiBktBoTUCWTqDYHpB",  # ustreamer
    "5TxBdkHpWERMx25w9gk7nALxsj462Ei56bUCuKNwkdQo",  # CG Stimmy
    "5U11yxEWRszr5BYCNciSvoxQ46GKB4edsTs3tNHarKSv",  # funded by suppo port1
    "3jJrMJFQ9m2b2dtKfemcgwTuAeWDjSh3UbgvGveZUvnK",  # CG money giga
    "HRmn3VsdS5kwJJF1uHJoHRiHQEXkT1jgzHKmTP7oiPFf",  # pk limit order
    "8L3giAGPuhtuZJrP5SXPc1SG1n22f1vqLNrMwt5RPwj3",  # fresh giga
    "aPvLrvGVWEU6gxPrcVHGsuoiwbY1orC7RBuGWm2HwNo",   # fresh giga2
    "9HmsRfR1WYdCbEffabkn2CfbMhnnQxTf8Uqd74vSJxUw",  # cg popdog1
    "BGR2CZTMuVzCN8nMeEekmGRGCr1WaH8rwUfgSAoXwKPj",  # suppo popdog
    "3fnFrzSRFfUtDotcYQgrZY9k6HKZXafDvW14struBi22",  # pk new phantom
    "7KRiBwhjUeLD4uG61UGYqh5CwkbH68M5TkbkgEAtkzq8",  # suppo oigon cnct
    "9v5ceZc1C3UzzWuy11wEsXuEncwZiVRPCrKjxv5vNT8o",  # suppo magic
    "EjF8xMovv4QBUKMpagTniy4G6RxaHHwzCrL5AKAKM2bK",  # suppo bridge from eth
    "7XTB95B9qXZPcCkaqs8TKaV1SkPNNPXGQEz1wAcnQjdu",  # suppo bridge
    "HpX2xQxo864Pn3N8a53yxWjCXQKV3s3QWv1w2a6meTw5",  # suppo bridge 2
    "Dm4gLzxotRj4csCXtFmRBbudAAnJPvbt3FLNJ7N1CSZh",  # Suppo Magic 3
    "DsTdm1j7vyLnzftpmyv5iAZfYcBpwagUKHUYwc2R65mB",  # Suppo Contra
    "AKxUREkAX7SMx3KfcN4DoTB8VWBaGT5SpRWo1QvaN4Aq",  # CG RI
    "ADEJ4dzXnD34J1SkwirvksZMYMTiabzNhBcJqn4td6nX",  # CG RI2
    "65Qfj1bzwZPJjGtLwcS72nXRRZcmFRcN7xstj4jFmnVg",  # RI CG?
    "9vpDUd66XScDynMys3eQmsgcXnCMZSjJrkuedXWLrAzo",  # RI CG2
    "28tMjRp8AFtQnfyTxMb8XUCXmMruz76kTC2QKmrrkYXL",  # ri cg3
    "B5oUKxsw84TdxsRczscwMrRnfv9ZMQkTzq3obsTs47Co",  # Suppo Harry 2
    "8bR9j2FikiFkThfHDYrNTG5JV165Mm71Fgkv7NRzLgNC",  # fried 2
    "wD4veK3LUfQeTa1TWR8oVU2tjmg6oLe9pwSEGtHsgmj",   # CG Rally
    "JBZcbw2YaJd7LLxjBVRxT3n1X6kjMPz1yvRLoVUCiFrx",  # PK - FRX
    "6gmW5CsGJuRYaRkLVoh8kTQCE7v4DJ9tpoeEaHZsVvYR",  # gadget goober fetchr1
    "Gk8pnC2xrKvnRQxHxv4VZ6Z4AiXPfpAhfKM88gSiRRb5",  # follower of sup
    "GdSFRvK8AKrPHkisWbTCjzjqFK2gGF919HF9qghP3kuu",  # cepryl
    "3S22MmmQPuJ6nUsKWRKyS82dGwxjf4H1cwqfMBHfsn6V",  # smartie
    "BM9CcyErJcu2mjrFvUsRRrD3snGeHDDVirJLvL6EjvMN",  # giant wallet
    "DV3NGC4mcptJVUBsQ5Am626YYtJPfZBF69XsjGenYiKv",  # CG Viral
    "41YadHSTLs3dXS6bC5kLEsX1MQjetyJqVRVLpW63upLt",  # suppo spom
    "BovY4yhUh8s6u9oiFnLQezwRTS2foevqH6KmbDiviYC9",  # cg payai
    "CYwxLpwHiJ81YGrnBbuhmLnqejUskn1XanwR6tZeEEaX",  # CG fu
    "42GnRwZyr1RsqofeEdayrCmAFbvpgyuwuKEoKEsjQbW6",  # test
    "4BhPzNRja1r7XJVD1kLFHx3z9zFiXhUhAsUCqAsN1acL",  # Suppo Print1
    "8CrJ5wyhsGbs1UZ74yBFzqtqBVjSUCi2mr8MXUmzsq91",  # Suppo Print2
    "3NV4JLiA3meQeSDQqpU6DxcsBVgPyC5rNKUA8dLefvqr",  # Suppo Print3
    "BBKGavUJoBUrarwtSPgCKwKFwuUzA9vEZCGPcuUDC7w3",  # Suppo Print4
    "AtzeX2TF1Epkg8DitmjW6Tg7A4QYmbQ2QyPY1igpayMJ",  # MAD CG
    "7Z15U9xpHeVUAe5b7dXrx3Z8Rq8qfLfN3ERNaE2zKpWh",  # CG Bored 3
    "F8GpobQGivx5P68dgXxAiPrQLb7Z9MEdP3p12p4QWHRt",  # CG Bart2
    "4FgcnDhKn3qEycuJfxvvQ5eKg6cAnHu2DfYeU6kQmgt5",  # CG bored
    "3haRTNqYsBT1U9o26XDvkRV6jxwiqbSPcqRkf4REp3Hn",  # CG bored2
    "6rcfuiUX445seYXr8yeZuMfwqbn8wTivPmoBJW1eU3C6",  # CG Pup Polywog
    "Fi2Ta5jWq5ttNRp1D3wXkeotJEA3J4nPTAVewbGubHUr",  # CG LMAO
    "3VnAKxxjn1wWv3S8wrN5enM3xksvCp2QqvofhHsMzD5f",  # CG polywog2
    "FBchxQhd3UesmJtdLqsBHK5wVTzwwCnZqffkP9HZQJwQ",  # Polywog Altszn
    "35VkqS77CDLEjgoegzbMf1MuzTtmhXSxQ4oLwePkeU6v",  # Print Altszn
    "5JgADWaAVpDib4cCM868Q2MdHfAAoUjZrzghB2YSg4C1",  # Cg Altszn
    "5oRNbpo9jSAhJsqiidUjnrF7DrnjgSKMZ9trXKHbmzpw"   # suppo for sure
]

# Stablecoins and baseline transit tokens filtered out of scans
SKIP_TOKENS = {
    "So11111111111111111111111111111111111111112",  # wSOL
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"   # USDT
}

# Institutional and Exchange cold/hot nodes to avoid parsing
EXCHANGE_WALLETS = {
    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "5tzFkiKscXHK5ZXCGbGuEgkrUjDA9b6AXetFnq5SxFBP",
    "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE",
    "H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS",
    "FWznbcNXWQuHTawe9RxvQ2LdCENssh12dsznf4RiouN5",
    "AC5RDfQFmDS1deWZos921JfqscXdByf8BKHs5ACWjtW2",
    "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm",
    "BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6",
    "8i5HqznCcCPaFLXyUNtPNM1sPQSCyR7D7BQYUURNE2iV",
    "2ojv9BAiHUrvsm9gxDe7fJSzbNZSJcxZvf8dqmWGHG8S",
    "Fc8SF1XqMqmxFrszJNAEKMbW8V6MNrDsmW5sFt2E9wfB",
    "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1",
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"
}