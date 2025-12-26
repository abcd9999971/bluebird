import { watch } from 'vue';

/**
 * Member Theme Composable
 * Manages the dynamic application of member-specific colors to CSS variables.
 * 
 * @param {Ref<string>} currentMemberKey - The currently selected member key (or null)
 * @param {Object} authors - Map of author objects containing color information
 * @param {string} defaultColor - The baseline brand color
 */
export function useMemberTheme(currentMemberKey, authors, defaultColor = '#1d9bf0') {

    // Helper to convert hex to RGB values for "rgba" manipulation in CSS if needed
    // (Though we are using color-mix in CSS, having RGB vars can be useful for older browsers or specific overlays)
    const hexToRgb = (hex) => {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    };

    /**
     * Applies the theme variables to the document root
     * @param {string} colorHex 
     */
    const applyThemeVariables = (colorHex) => {
        const root = document.documentElement;
        root.style.setProperty('--brand-color', colorHex);

        // Set a "dim" version for backgrounds
        // Note: detailed mixing is done in CSS via color-mix(), but we set the base here.

        // Optional: We could set --bg-stripe-base-color here explicitly if needed, 
        // but the CSS watcher for data-member-theme handles switching between brand-blue and brand-color.
    };

    /**
     * Watcher to update theme when member changes
     */
    watch(currentMemberKey, (newKey) => {
        const isMemberSelected = !!(newKey && authors[newKey]);

        // Toggle the data attribute for CSS selectors
        document.documentElement.dataset.memberTheme = isMemberSelected;

        if (isMemberSelected) {
            const memberColor = authors[newKey].color;
            applyThemeVariables(memberColor);
        } else {
            applyThemeVariables(defaultColor);
        }
    }, { immediate: true });

    return {
        applyThemeVariables
    };
}
