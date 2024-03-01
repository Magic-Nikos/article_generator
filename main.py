import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox
import generate as g

# Initialisation de l'interface CustomTkinter
ctk.set_appearance_mode("dark")  # Choix du thème ('Light' ou 'Dark')
ctk.set_default_color_theme("green")  # Choix du thème de couleur

class BlogPublisher(ctk.CTk):

    number = 1

    def __init__(self):
        super().__init__()

        self.title('Blog Publisher')
        self.geometry('1050x450')

        self.setup_frame = ctk.CTkFrame(self)
        self.setup_frame.pack(pady=(20, 10), padx=20, fill="x", expand=True)

        self.blog_path_button = ctk.CTkButton(self.setup_frame, text='Choisir le dossier du blog', command=self.choose_blog_path)
        self.blog_path_button.pack(side='left', padx=(0, 20))

        default_blog_path = '/home/colonel/fait-main'
        self.blog_path_label = ctk.CTkLabel(self.setup_frame, text=default_blog_path)
        self.blog_path_label.pack(side='left', padx=(0, 20))

        self.blog_type_switch = ctk.CTkSwitch(self.setup_frame, text='Hexo')
        self.blog_type_switch.pack(side='right')

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=(20, 10), padx=20, fill="x")

        self.category_label = ctk.CTkLabel(self.top_frame, text='Catégorie:')
        self.category_label.pack(side='left', padx=(0, 20))

        self.category_entry = ctk.CTkEntry(self.top_frame, width=200)
        self.category_entry.pack(side='left')

        self.tags_label = ctk.CTkLabel(self.top_frame, text='Tags:')
        self.tags_label.pack(side='left', padx=(20, 20))

        self.tags_entry = ctk.CTkEntry(self.top_frame, width=200)
        self.tags_entry.pack(side='left')

        self.article_count_label = ctk.CTkLabel(self.top_frame, text="Nombre d'articles:")
        self.article_count_label.pack(side='left', padx=(20, 5))

        self.article_count_slider = ctk.CTkSlider(self.top_frame, from_=1, to=50, width=150, command=self.update_article_count_label)
        self.article_count_slider.set(1)
        self.article_count_slider.pack(side='left')

        # Mettez à jour le label après la création du slider pour éviter AttributeError
        self.article_count_value_label = ctk.CTkLabel(self.top_frame, text=f'{self.article_count_slider.get():.0f}')
        self.article_count_value_label.pack(side='left', padx=(5, 20))

        self.generate_button = ctk.CTkButton(self.top_frame, text='Générer Sujets', command=self.generate_subjects)
        self.generate_button.pack(side='left', padx=(20, 0))

        # Cadre et widget pour les sujets
        self.subjects_label = ctk.CTkLabel(self, text='Sujets (éditable):')
        self.subjects_label.pack(pady=(10, 5))

        self.subjects_text = scrolledtext.ScrolledText(self, height=10)
        self.subjects_text.pack(pady=(0, 20), padx=20)

        # Cadre pour les boutons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=(10, 20), padx=20, fill="x")

        # Cadre interne pour centrer les boutons dans le cadre principal
        self.inner_button_frame = ctk.CTkFrame(self.button_frame)
        self.inner_button_frame.pack(expand=True, pady=10)

        # Bouton Générer
        self.generate_button = ctk.CTkButton(self.inner_button_frame, text='Générer', command=self.generate_articles)
        self.generate_button.pack(side='left', padx=10)  # Espacement entre les boutons

        # Bouton Publier
        self.publish_button = ctk.CTkButton(self.inner_button_frame, text='Publier', command=self.publish_articles)
        self.publish_button.pack(side='left')

    def update_article_count_label(self, event=None):
        self.number = int(self.article_count_slider.get())
        self.article_count_value_label.configure(text=f'{self.article_count_slider.get():.0f}')

    def get_and_print_subjects(self):
        subjects_text = self.subjects_text.get("1.0", "end-1c")
        subjects_array = subjects_text.split('\n')
        subjects_array = [title for title in subjects_array if title.strip()]
        print(subjects_array)
        return subjects_array

    def publish_articles(self):
        subjects = self.get_and_print_subjects()

    def choose_blog_path(self):
        # Fonction pour choisir le dossier du blog
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.blog_path_label.configure(text=folder_selected)
            # Ici, vous pouvez également mettre à jour le chemin du projet de votre script

    def toggle_blog_type(self):
        # Fonction pour basculer entre Hexo et Jekyll
        if self.blog_type_switch.get() == 1:  # Si le switch est activé
            self.blog_type_switch.configure(text='Jekyll')
            # Mettre à jour les paramètres ou les variables de votre script pour Jekyll
        else:
            self.blog_type_switch.configure(text='Hexo')
            # Mettre à jour les paramètres ou les variables de votre script pour Hexo

    def generate_subjects(self):
        category = self.category_entry.get()
        if not category:
            messagebox.showerror("Erreur", "Veuillez entrer une catégorie.")
            return ""
        titles_text = g.titles_generation(self.number, category)
        if titles_text is None:
            messagebox.showerror("Erreur", "Aucun titre généré")
            return
        titles = titles_text.split('\n')
        formatted_titles = [title.split('. ', 1)[-1] for title in titles if title.strip()]
        # Supprimer tous les '- ' de chaque titre
        formatted_titles = [title.replace('- ', '') for title in formatted_titles]
        formatted_titles_str = '\n'.join(formatted_titles)
        self.subjects_text.delete('1.0', 'end')
        self.subjects_text.insert('1.0', formatted_titles_str)

    def generate_articles(self):
        # Récupérer les informations nécessaires
        subjects_text = self.subjects_text.get("1.0", "end-1c")
        subjects_array = [title.strip() for title in subjects_text.split('\n') if title.strip()]
        blog_path = self.blog_path_label.cget("text")
        category = self.category_entry.get()
        category = self.category_entry.get().replace(' ', '-')
        print(category)
        if not category:
            messagebox.showerror("Erreur", "Veuillez entrer une catégorie.")
            return
        tags_text = self.tags_entry.get()
        tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        blog_type = 'Hexo' if self.blog_type_switch.get() == 0 else 'Jekyll'

        # Traiter chaque sujet individuellement
        for sujet in subjects_array:
            try:
                g.create_and_publish_article(blog_path, sujet, tags, category, blog_type)
            except Exception as e:
                messagebox.showerror("Erreur",
                                     f"Erreur lors de la création ou de la publication de l'article: {sujet}\n{e}")
                return  # Arrêtez de traiter d'autres titres après la première erreur

        messagebox.showinfo("Succès", "Tous les articles ont été créés et publiés avec succès.")


# Exécution de l'interface graphique
if __name__ == "__main__":
    app = BlogPublisher()
    app.mainloop()
