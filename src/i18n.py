import locale
import os

TRANSLATIONS = {
    "en": {
        # History Window
        "app_subtitle_default": "Clipboard History",
        "app_subtitle_empty": "Clipboard is empty",
        "app_subtitle_counts": "{total} items • {pinned} pinned",
        "app_subtitle_counts_single": "{total} items",
        "tooltip_show_pinned": "Show only pinned items",
        "tooltip_settings": "Settings",
        "tooltip_clear_history": "Clear history (keeps pinned items)",
        "search_placeholder": "Search clipboard... (type to filter)",
        "empty_search_title": "No results",
        "empty_search_desc": 'No clipboard item contains "{query}".',
        "empty_pinned_title": "No pinned items",
        "empty_pinned_desc": "Pin items using the pin button to keep them here.",
        "empty_history_title": "Clipboard is empty",
        "empty_history_desc": "Copy text with Ctrl+C to save it here.",
        "meta_pinned": "Pinned",
        "meta_pinned_with_time": "Pinned • {time}",
        "tooltip_pin": "Pin to top (Ctrl+P)",
        "tooltip_unpin": "Unpin (Ctrl+P)",
        "tooltip_delete": "Delete (Del)",
        "empty_clip": "<Empty>",
        "time_now": "Just now",
        "time_mins_ago": "{n}m ago",
        "time_hours_ago": "{n}h ago",
        "time_yesterday": "Yesterday",
        "time_days_ago": "{n}d ago",

        # Settings Window
        "settings_title": "Pasty Settings",
        "page_general": "General",
        "group_shortcuts": "Keyboard Shortcuts",
        "group_shortcuts_desc": "Quickly access and manage your clips.",
        "row_global_shortcut_title": "Global Shortcut (Alt+V)",
        "row_global_shortcut_sub": (
            "Go to Settings > Keyboard > View and Customize Shortcuts > Custom Shortcuts.\n"
            "Add a new shortcut running the 'pasty.sh' script.\n"
            "Tip: Alt+V is recommended on GNOME to avoid conflicts with the Super key."
        ),
        "row_inapp_shortcuts_title": "In-app shortcuts",
        "row_inapp_shortcuts_sub": (
            "• Type anytime to search\n"
            "• Up/Down arrows + Enter (or Alt+1..9) to copy\n"
            "• Ctrl+P to pin/unpin • Del to delete"
        ),
        "group_history": "Clipboard History",
        "row_history_size_title": "History Size",
        "row_history_size_sub": "Maximum number of unpinned items to store",
        "group_about": "About",
        "row_developer": "Developed by",
        "row_github": "GitHub",
        "row_contact": "Contact",
    },
    "it": {
        # History Window
        "app_subtitle_default": "Cronologia appunti",
        "app_subtitle_empty": "Cronologia vuota",
        "app_subtitle_counts": "{total} elementi • {pinned} fissati",
        "app_subtitle_counts_single": "{total} elementi",
        "tooltip_show_pinned": "Mostra solo elementi fissati",
        "tooltip_settings": "Impostazioni",
        "tooltip_clear_history": "Cancella cronologia (mantiene i fissati)",
        "search_placeholder": "Cerca negli appunti... (digita per filtrare)",
        "empty_search_title": "Nessun risultato",
        "empty_search_desc": 'Nessun appunto contiene "{query}".',
        "empty_pinned_title": "Nessun elemento fissato",
        "empty_pinned_desc": "Fissa gli appunti con l'icona spilla per ritrovarli sempre qui.",
        "empty_history_title": "Cronologia vuota",
        "empty_history_desc": "Copia del testo con Ctrl+C per salvarlo qui.",
        "meta_pinned": "Fissato",
        "meta_pinned_with_time": "Fissato • {time}",
        "tooltip_pin": "Fissa in alto (Ctrl+P)",
        "tooltip_unpin": "Rimuovi dai fissati (Ctrl+P)",
        "tooltip_delete": "Elimina (Canc)",
        "empty_clip": "<Vuoto>",
        "time_now": "Adesso",
        "time_mins_ago": "{n}m fa",
        "time_hours_ago": "{n}h fa",
        "time_yesterday": "Ieri",
        "time_days_ago": "{n}g fa",

        # Settings Window
        "settings_title": "Impostazioni Pasty",
        "page_general": "Generale",
        "group_shortcuts": "Scorciatoie da Tastiera",
        "group_shortcuts_desc": "Accedi e gestisci rapidamente la cronologia.",
        "row_global_shortcut_title": "Scorciatoia Globale (Alt+V)",
        "row_global_shortcut_sub": (
            "Vai in Impostazioni > Tastiera > Scorciatoie personalizzate.\n"
            "Aggiungi una scorciatoia che esegue lo script 'pasty.sh'.\n"
            "Consiglio: Alt+V è ideale su GNOME per evitare conflitti con il tasto Super."
        ),
        "row_inapp_shortcuts_title": "Comandi rapidi nella finestra",
        "row_inapp_shortcuts_sub": (
            "• Digita per cercare istantaneamente\n"
            "• Frecce Su/Giù + Invio (o Alt+1..9) per copiare\n"
            "• Ctrl+P per fissare/rimuovere un appunto • Canc per eliminare"
        ),
        "group_history": "Cronologia Appunti",
        "row_history_size_title": "Dimensione Cronologia",
        "row_history_size_sub": "Numero massimo di appunti non fissati da mantenere",
        "group_about": "Informazioni",
        "row_developer": "Sviluppato da",
        "row_github": "GitHub",
        "row_contact": "Contatto",
    },
    "fr": {
        # History Window
        "app_subtitle_default": "Historique du presse-papiers",
        "app_subtitle_empty": "Historique vide",
        "app_subtitle_counts": "{total} éléments • {pinned} épinglés",
        "app_subtitle_counts_single": "{total} éléments",
        "tooltip_show_pinned": "Afficher uniquement les éléments épinglés",
        "tooltip_settings": "Paramètres",
        "tooltip_clear_history": "Effacer l'historique (garde les épinglés)",
        "search_placeholder": "Rechercher dans le presse-papiers...",
        "empty_search_title": "Aucun résultat",
        "empty_search_desc": 'Aucun élément ne contient "{query}".',
        "empty_pinned_title": "Aucun élément épinglé",
        "empty_pinned_desc": "Épinglez des éléments pour les conserver ici.",
        "empty_history_title": "Presse-papiers vide",
        "empty_history_desc": "Copiez du texte avec Ctrl+C pour le voir apparaître ici.",
        "meta_pinned": "Épinglé",
        "meta_pinned_with_time": "Épinglé • {time}",
        "tooltip_pin": "Épingler en haut (Ctrl+P)",
        "tooltip_unpin": "Détacher (Ctrl+P)",
        "tooltip_delete": "Supprimer (Suppr)",
        "empty_clip": "<Vide>",
        "time_now": "À l'instant",
        "time_mins_ago": "Il y a {n} min",
        "time_hours_ago": "Il y a {n} h",
        "time_yesterday": "Hier",
        "time_days_ago": "Il y a {n} j",

        # Settings Window
        "settings_title": "Paramètres de Pasty",
        "page_general": "Général",
        "group_shortcuts": "Raccourcis clavier",
        "group_shortcuts_desc": "Accédez rapidement à vos éléments copiés.",
        "row_global_shortcut_title": "Raccourci global (Alt+V)",
        "row_global_shortcut_sub": (
            "Allez dans Paramètres > Clavier > Raccourcis personnalisés.\n"
            "Ajoutez un raccourci exécutant le script 'pasty.sh'.\n"
            "Astuce : Alt+V est recommandé sous GNOME pour éviter les conflits avec la touche Super."
        ),
        "row_inapp_shortcuts_title": "Commandes dans l'application",
        "row_inapp_shortcuts_sub": (
            "• Saisissez du texte pour rechercher instantanément\n"
            "• Flèches Haut/Bas + Entrée (ou Alt+1..9) pour copier\n"
            "• Ctrl+P pour épingler/détacher • Suppr pour effacer"
        ),
        "group_history": "Historique du presse-papiers",
        "row_history_size_title": "Taille de l'historique",
        "row_history_size_sub": "Nombre maximal d'éléments non épinglés à conserver",
        "group_about": "À propos",
        "row_developer": "Développé par",
        "row_github": "GitHub",
        "row_contact": "Contact",
    },
    "es": {
        # History Window
        "app_subtitle_default": "Historial del portapapeles",
        "app_subtitle_empty": "Historial vacío",
        "app_subtitle_counts": "{total} elementos • {pinned} fijados",
        "app_subtitle_counts_single": "{total} elementos",
        "tooltip_show_pinned": "Mostrar solo elementos fijados",
        "tooltip_settings": "Configuración",
        "tooltip_clear_history": "Borrar historial (mantiene los fijados)",
        "search_placeholder": "Buscar en el portapapeles... (escribe para filtrar)",
        "empty_search_title": "Sin resultados",
        "empty_search_desc": 'Ningún elemento contiene "{query}".',
        "empty_pinned_title": "No hay elementos fijados",
        "empty_pinned_desc": "Fija elementos con el botón de chincheta para mantenerlos aquí.",
        "empty_history_title": "Portapapeles vacío",
        "empty_history_desc": "Copia texto con Ctrl+C para guardarlo aquí.",
        "meta_pinned": "Fijado",
        "meta_pinned_with_time": "Fijado • {time}",
        "tooltip_pin": "Fijar arriba (Ctrl+P)",
        "tooltip_unpin": "Desfijar (Ctrl+P)",
        "tooltip_delete": "Eliminar (Supr)",
        "empty_clip": "<Vacío>",
        "time_now": "Ahora",
        "time_mins_ago": "Hace {n} min",
        "time_hours_ago": "Hace {n} h",
        "time_yesterday": "Ayer",
        "time_days_ago": "Hace {n} d",

        # Settings Window
        "settings_title": "Configuración de Pasty",
        "page_general": "General",
        "group_shortcuts": "Atajos de teclado",
        "group_shortcuts_desc": "Accede y gestiona rápidamente tus elementos.",
        "row_global_shortcut_title": "Atajo global (Alt+V)",
        "row_global_shortcut_sub": (
            "Ve a Configuración > Teclado > Atajos personalizados.\n"
            "Añade un atajo que ejecute el script 'pasty.sh'.\n"
            "Consejo: Se recomienda Alt+V en GNOME para evitar conflictos con la tecla Super."
        ),
        "row_inapp_shortcuts_title": "Comandos en la ventana",
        "row_inapp_shortcuts_sub": (
            "• Escribe para buscar al instante\n"
            "• Flechas Arriba/Abajo + Enter (o Alt+1..9) para copiar\n"
            "• Ctrl+P para fijar/desfijar • Supr para eliminar"
        ),
        "group_history": "Historial del portapapeles",
        "row_history_size_title": "Tamaño del historial",
        "row_history_size_sub": "Número máximo de elementos no fijados a conservar",
        "group_about": "Acerca de",
        "row_developer": "Desarrollado por",
        "row_github": "GitHub",
        "row_contact": "Contacto",
    },
    "de": {
        # History Window
        "app_subtitle_default": "Zwischenablage-Verlauf",
        "app_subtitle_empty": "Verlauf ist leer",
        "app_subtitle_counts": "{total} Einträge • {pinned} angeheftet",
        "app_subtitle_counts_single": "{total} Einträge",
        "tooltip_show_pinned": "Nur angeheftete Einträge anzeigen",
        "tooltip_settings": "Einstellungen",
        "tooltip_clear_history": "Verlauf leeren (behält angeheftete)",
        "search_placeholder": "Zwischenablage durchsuchen...",
        "empty_search_title": "Keine Ergebnisse",
        "empty_search_desc": 'Kein Eintrag enthält "{query}".',
        "empty_pinned_title": "Keine angehefteten Einträge",
        "empty_pinned_desc": "Heften Sie Einträge an, um sie dauerhaft hier zu behalten.",
        "empty_history_title": "Zwischenablage ist leer",
        "empty_history_desc": "Kopieren Sie Text mit Strg+C, um ihn hier zu speichern.",
        "meta_pinned": "Angeheftet",
        "meta_pinned_with_time": "Angeheftet • {time}",
        "tooltip_pin": "Oben anheften (Strg+P)",
        "tooltip_unpin": "Lösen (Strg+P)",
        "tooltip_delete": "Löschen (Entf)",
        "empty_clip": "<Leer>",
        "time_now": "Gerade eben",
        "time_mins_ago": "vor {n} Min.",
        "time_hours_ago": "vor {n} Std.",
        "time_yesterday": "Gestern",
        "time_days_ago": "vor {n} Tagen",

        # Settings Window
        "settings_title": "Pasty Einstellungen",
        "page_general": "Allgemein",
        "group_shortcuts": "Tastaturkürzel",
        "group_shortcuts_desc": "Schneller Zugriff auf Zwischenablage-Einträge.",
        "row_global_shortcut_title": "Globaler Shortcut (Alt+V)",
        "row_global_shortcut_sub": (
            "Öffnen Sie Einstellungen > Tastatur > Tastaturkürzel anpassen > Eigene Kürzel.\n"
            "Fügen Sie ein Kürzel hinzu, das 'pasty.sh' ausführt.\n"
            "Tipp: Unter GNOME wird Alt+V empfohlen, um Konflikte mit der Super-Taste zu vermeiden."
        ),
        "row_inapp_shortcuts_title": "Kürzel im Fenster",
        "row_inapp_shortcuts_sub": (
            "• Einfach tippen, um sofort zu suchen\n"
            "• Pfeiltasten Hoch/Runter + Eingabetaste (oder Alt+1..9) zum Kopieren\n"
            "• Strg+P zum Anheften/Lösen • Entf zum Löschen"
        ),
        "group_history": "Zwischenablage-Verlauf",
        "row_history_size_title": "Verlaufsgröße",
        "row_history_size_sub": "Maximale Anzahl nicht angehefteter Einträge",
        "group_about": "Über",
        "row_developer": "Entwickelt von",
        "row_github": "GitHub",
        "row_contact": "Kontakt",
    },
}


def get_system_language():
    """Detect the system language code (e.g. 'en', 'it', 'fr', 'es', 'de')."""
    # Check standard environment variables first
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var)
        if val:
            code = val.split(".")[0].split("_")[0].lower()
            if code in TRANSLATIONS:
                return code

    # Fallback to Python's locale module
    try:
        loc = locale.getdefaultlocale()[0]
        if loc:
            code = loc.split("_")[0].lower()
            if code in TRANSLATIONS:
                return code
    except Exception:
        pass

    return "en"


CURRENT_LANG = get_system_language()


def _(key, **kwargs):
    """Retrieve translated string with optional formatting."""
    lang_dict = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

