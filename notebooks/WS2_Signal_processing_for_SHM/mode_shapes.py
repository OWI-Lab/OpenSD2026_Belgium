
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# ============== SAFE PRECOMPUTATION (FAST) =================
# ==========================================================
def prepare_mode_shapes(mode_shapes):
    """
    mode_shapes: (n_orders, n_models, 6)
    Returns normalized FA & SS magnitudes for each order & model.
    """

    # Extract FA and SS DOFs
    FA_idx = np.array([0, 2, 4])
    SS_idx = np.array([1, 3, 5])

    FA = np.real(mode_shapes[:, :, FA_idx])
    SS = np.real(mode_shapes[:, :, SS_idx])

    # ---------- SAFE max without warnings ----------
    # If slice is all-NaN → define max=1
    max_FA = np.nanmax(np.where(np.isnan(FA), -np.inf, np.abs(FA)), axis=2, keepdims=True)
    max_FA[~np.isfinite(max_FA)] = 1  # handles all-NaN slices

    max_SS = np.nanmax(np.where(np.isnan(SS), -np.inf, np.abs(SS)), axis=2, keepdims=True)
    max_SS[~np.isfinite(max_SS)] = 1  # handles all-NaN slices

    # ---------- Normalize ----------
    FA_norm = FA / max_FA
    SS_norm = SS / max_SS

    return FA_norm, SS_norm



# ==========================================================
# ============ STATIC MODE-SHAPE PLOTTER (FIXED) ===========
# ==========================================================
def plot_static_mode_shape(
        target_freq,
        tol,
        ssi_order,
        # lscf_order,
        SSI_mode_shapes,
        SSI_freqs,
        # LSCF_mode_shapes,
        # LSCF_freqs
):
    # ---------- Elevations with mudline ----------
    LAT = np.array([-50, 15, 69, 97])

    # ---------- Precompute normalized shapes ----------
    SSI_FA, SSI_SS = prepare_mode_shapes(SSI_mode_shapes)
    # LSCF_FA, LSCF_SS = prepare_mode_shapes(LSCF_mode_shapes)

    # prepend mudline zero
    SSI_FA = np.concatenate([np.zeros((SSI_FA.shape[0], SSI_FA.shape[1], 1)), SSI_FA], axis=2)
    SSI_SS = np.concatenate([np.zeros((SSI_SS.shape[0], SSI_SS.shape[1], 1)), SSI_SS], axis=2)
    # LSCF_FA = np.concatenate([np.zeros((LSCF_FA.shape[0], LSCF_FA.shape[1], 1)), LSCF_FA], axis=2)
    # LSCF_SS = np.concatenate([np.zeros((LSCF_SS.shape[0], LSCF_SS.shape[1], 1)), LSCF_SS], axis=2)

    # ---------- Get frequencies for chosen orders ----------
    ssi_freq_list = SSI_freqs[ssi_order]
    # lscf_freq_list = LSCF_freqs[lscf_order]

    # ---------- Select matching frequencies ----------
    idx_ssi = np.where(np.abs(ssi_freq_list - target_freq) <= tol)[0]
    # idx_lscf = np.where(np.abs(lscf_freq_list - target_freq) <= tol)[0]

    if len(idx_ssi) == 0:
        print("⚠ No SSI mode within tolerance.")
        return
    # if len(idx_lscf) == 0:
    #     print("⚠ No LSCF mode within tolerance.")
    #     return

    # pick first matches
    idx_ssi = idx_ssi[0]
    # idx_lscf = idx_lscf[0]

    f_ssi = ssi_freq_list[idx_ssi]
    # f_lscf = lscf_freq_list[idx_lscf]

    # ======================================================
    # ===================== PLOT ===========================
    # ======================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))

    # ---------- FA ----------
    ax1.plot(np.abs(SSI_FA[ssi_order, idx_ssi]), LAT, "o-", label=f"SSI {f_ssi:.3f} Hz")
    #   ax1.plot(np.abs(LSCF_FA[lscf_order, idx_lscf]), LAT, "s-", label=f"LSCF {f_lscf:.3f} Hz")
    ax1.axhline(0, color='b', label="SWL")
    ax1.set_title("Fore–Aft (FA)")
    ax1.set_xlabel("Normalized amplitude")
    ax1.set_ylabel("Elevation [m]")
    ax1.legend()

    # ---------- SS ----------
    ax2.plot(np.abs(SSI_SS[ssi_order, idx_ssi]), LAT, "o--", label=f"SSI {f_ssi:.3f} Hz")
    # ax2.plot(np.abs(LSCF_SS[lscf_order, idx_lscf]), LAT, "s--", label=f"LSCF {f_lscf:.3f} Hz")
    ax2.axhline(0, color='b', label="SWL")
    ax2.set_title("Side–Side (SS)")
    ax2.set_xlabel("Normalized amplitude")
    ax2.legend()

    plt.show()
