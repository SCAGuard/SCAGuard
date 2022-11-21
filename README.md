# Table of contents
* [1. Server Applications](#1-server-applications)
* [2. Code Mutation](#2-code-mutation)
* [3. 5 Scenarios in RQ2](#3-5-scenarios-in-rq2)
* [4. Sample selection in RQ3](#4-sample-selection-in-rq3)
* [Reference](#reference)


# 1. Server Applications 

In this paper, we also collect various server applications as part of benign dataset, because the server scenarios are often compromised due to CSCAs. For each typical category of server applications from prior work in security community [A]–[D], we choose one of the most commonly-used real-world applications, namely, SQLite [E] (Database), OpenSSH [F] (SSH
Server), OpenSSL (Transport Encryption) [G], Vsftpd [H] (FTP server), Thttpd [I] (Web server), Gzip [J] (HTTP Compression), OpenVPN [K] (VPN Server), OpenNTPD [L] (Network Time Protocol Implementation).

# 2. Code Mutation

Following the recent works [M-P], we conduct the mutation technique to expand the diversity and number of our attack samples.  In this paper, we use an open source tool Mutate++ (https://github.com/nlohmann/mutate_cpp) to mutate the attack code. The tool randomly selects at least one of the 12  mutation operations, such as "Replaces logical operator", "Swaps increment and decrement operators", etc and perform them on different attack implementations . Note that we retain the attack functionality during mutation so that the code mutation does not fundamentally break the attack behaviors.



# 3. 5 Scenarios in RQ2

To evaluate the effectiveness of SCAGUARD, we consider five different scenarios, as summarized in Table V.

#### S1: Different implementations of the same attack. 

Attackers can implement the same attack and attack strategy (i.e., vulnerability exploitation) in different ways, leading to dissimilar programs. We randomly choose 2 different implementations from FR-IAIK, FR-Mastik, FR-Nepoche and their mutated variants (cf. Table II) and measure their similarity degree (repeat 300 times). The resulting average similarity score is 94.31%, indicating that SCAGUARD can show that different implementations of the same attack are tightly similar.

#### S2: Different variants of the same attack. 
Attackers may adopt different attack strategies to achieve the same functionality in order to bypass certain defenses. Recall that instead of using the flush instruction in the Flush+Reload attack, the Evict+Reload attack uses another way to evict corresponding cache lines of the chosen memory addresses. To evaluate our approach in this scenario, we randomly choose 1 PoC from FR-IAIK, FR-Mastik, FR-Nepoche, and their variants, and measure its similarity with 1 randomly chosen sample from ER-IAIK and its mutated variants. Those two PoCs respectively implement the Flush+Reload and Evict+Reload attacks. We repeat the above experiment 300 times and calculate their average similarity. The resulting average similarity score produced by SCAGUARD is still very high, i.e., 84.32%, because of similar cache behaviors.

#### S3: Different attacks that exploit the same vulnerability.
There are different attacks all of which exploit the same cache side-channel vulnerability. For instance, the Flush+Reload and Prime+Probe attacks are two different attacks but exploit the vulnerability. To evaluate our approach in this scenario, we randomly choose 1 PoC from FR-IAIK, FR-Mastik, FR-Nepoche and their variants, and then measure its similarity with 1 randomly chosen PoC from PP-IAIK, PP-Jzhang, and their mutated samples (repeat 300 times). The resulting average similarity score is significant, i.e., 74.48%, because they both access the target cache lines and record the access time.

#### S4: Different variants that exploit different vulnerabilities. 
The newly proposed Meltdown and Spectre attacks can leverage traditional cache side-channel attacks. We randomly choose 1 PoC from FR-IAIK, FR-Mastik, FR-Nepoche and their mutated variants, and then measure its similarity with 1 Spectre-like variant randomly chosen from Spectre-FR-Kocher, Spectre-FR-Opsxcq, Spectre-FR-Idea4good, and their mutated variants (repeat 300 times). The resulting average similarity score produced by SCAGUARD is 66.92%, indicating that although the program is largely changed due to the introduction of Spectre, our approach can still show that these two attacks are closely related with each other.

#### S5: The similarity between an attack program and a benign program. 
An attack detection approach should not misclassify a benign program as an attack program. To evaluate our approach, we randomly choose a test case from the benign dataset (cf. Table III) as the benign program and compare its similarity with a randomly chosen PoC from FR-IAIK, FR-Mastik, FR-Nepoche, and their variants (repeat 300 times). It is interesting to see the average similarity score between them is only 15.10%, which is significantly lower than the similarity degrees between attack programs as reported above. 



# 4. Sample selection in RQ3

#### E1: Classification of mutated-variants. 
The mutated-variant classification task is to classify mutated variants when some
of them are known to the defender. The details are as follows:
- SVM-NW, LR-NW and KNN-MLFM: we perform 10-fold cross validation on 4 attack types (i.e., FR-F, PPF, S-FR and S-PP) and benign programs to obtain the best model with the fine-tuned parameters.
- SCAGUARD: we randomly choose only 1 PoC for each of 4 attack types for attack behavior modeling. 
- SCADET: uses its designated rules.

Then, let the trained models, SCAGuard, and SCADET classify the 40×5 samples that randomly chosen from FR-F, PPF, S-FR, S-PP and benign programs (40 samples were chosen for each type). 

#### E2: Classification of Spectre-like variants. 
The Spectre-like variant classification task is to classify spectre-like variants when only their non-spectre-like counterparts are known to the defender. The details are as follows:
- SVM-NW, LR-NW and KNN-MLFM: we train the models with FR-F and PP-F and 360 benign programs to their best performance. 
- SCAGUARD: we randomly choose only 1 PoC for each attack type of FR-F and PP-F for attack behavior modeling.
- SCADET: uses its designated rules.

Then, 40 PoCs from each attack type of S-FR and S-PP and 40 benign programs are randomly chosen for classification. 

#### E3: Classification of other attack family’s variants (Generalizability). 
To evaluate the generalizability of SCAGUARD, we consider two sub-tasks. The first one is to classify Prime+Probe Family when only the Flush+Reload Family is known to the defender. The details are as follows:

- SVM-NW, LR-NW and KNN-MLFM: we use the samples in FR-F and benign programs for training.
- SCAGUARD: we randomly choose 1 PoC of the attack type FR-F for attack behavior modeling. 
- SCADET: uses its designated rules.

Then we randomly choose 40 PoCs of the attack type PP-F and 40 benign programs for classification.

The second one is to classify Flush+Reload Family when only Prime+Probe Family is known to the defender. Details are as follows:

- SVM-NW, LR-NW and KNN-MLFM: we use the samples in PP-F and 360 benign programs for training.
- SCAGUARD: we randomly choose 1 PoC of the attack type PP-F for attack behavior modeling. 
- SCADET: uses its designated rules.

Similarly, then we randomly choose 40 PoCs of the attack type FR-F and 40 benign programs for classification.

#### E4: Classification of obfuscated variants (Robustness). 
To evaluate the robustness of SCAGUARD against a powerful attacker who tries to obfuscate an existing PoC in order to bypass the detection approach, for each PoC out of 400 PoCs of the attack type FR-F (resp. PP-F), we generate an obfuscated variant by applying the commonly-used obfuscation technique, polymorphic technique [69], resulting 400×2 new obfuscated variants. These obfuscated variants have, on average, 70.49% more BBs per sample than the original one. Our goal is to detect the obfuscated variants while only their non-obfuscated counterparts are known to the defender.

- SVM-NW, LR-NW and KNN-MLFM: we train the model on the FR-F, and PP-F, and benign programs.
- SCAGUARD: we randomly choose one PoC for each attack type of FR-F and PP-F for attack behavior modeling. 
- SCADET: uses its designated rules.

Then, We also randomly choose 40 obfuscated variants for each attack type of FR-F, and PP-F and 40 benign programs for classification.

# Reference

- **[A]** S. Proskurin et al., “xmp: Selective memory protection for kernel and user space,” in S&P, 2020.
- **[B]** H. Xue et al., “MORPH: enhancing system security through interactive customization of application and communication protocol features,” in CCS, 2018.
- **[C]** D. Xu et al., “Vmhunt: A verifiable approach to partially-virtualized binary code simplification,” in CCS, 2018.
- **[D]** U. Shankar et al., “Toward automated information-flow integrity verifi- cation for security-critical applications,” in NDSS, 2006.
- **[E]** Sqlite. Available: https://www.sqlite.org/download.html
- **[F]** Openssh. Available: https://github.com/openssh/openssh-portable
- **[G]** Openssl. Available: https://github.com/openssl/openssl
- **[H]** Vsftpd. Available: https://security.appspot.com/vsftpd.html
- **[I]** Thttpd. Available: https://acme.com/software/thttpd
- **[J]** Gzip. Available: https://www.gnu.org/software/gzip/
- **[K]** Openvpn. Available: https://openvpn.net/community-downloads/
- **[L]** Openntpd. Available: https://github.com/openntpd-portable/openntpd-portable
- **[M]** D. Moghimi, M. Lipp, B. Sunar, and M. Schwarz, “Medusa: Microarchitectural data leakage via automated attack synthesis,” in Proceedings of the 29th USENIX Security Symposium, 2020, pp. 1427–1444.
- **[N]** O. Oleksenko, B. Trach, M. Silberstein, and C. Fetzer, “Specfuzz:Bringing spectre-type vulnerabilities to the surface,” in Proceedings of the 29th USENIX Security Symposium, 2020, pp. 1481–1498.
- **[O]** M. C. Tol, B. G ̈ulmezoglu, K. Yurtseven, and B. Sunar, “Fastspec:Scalable generation and detection of spectre gadgets using neural embeddings,” in Proceedings of the IEEE European Symposium on Security and Privacy, 2021, pp. 616–632.
- **[P]** A. Alsaheel, Y. Nan, S. Ma, L. Yu, G. Walkup, Z. B. Celik, X. Zhang, and D. Xu, “ATLAS: A sequence-based learning approach for attack investigation,” in Proceedings of the 30th USENIX Security Symposium, 2021, pp. 3005–3022.
