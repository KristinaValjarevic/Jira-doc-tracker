import tkinter as tk
from tkinter import ttk
import webbrowser


class InitialView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Jira Documentation Tracker")
        ttk.Button(self, text="Add a New Project", command=self.add_project) \
            .grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(self, text="Update the Sheet", command=self.update_sheets) \
            .grid(row=0, column=1, pady=20)
        ttk.Button(self, text="Review Jira Issues", command=self.review_issues) \
            .grid(row=0, column=2, padx=20, pady=20)

    def add_project(self):
        self.destroy()
        NewProject(self.parent).pack(side="top", fill="both", expand=True)

    def update_sheets(self):
        self.destroy()
        UpdateSheets(self.parent).pack(side="top", fill="both", expand=True)

    def review_issues(self):
        self.destroy()
        JiraIssues(self.parent).pack(side="top", fill="both", expand=True)


class SecondaryView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.back_button = ttk.Button(self, text="Back", command=self.back)

    def back(self):
        self.destroy()
        InitialView(self.parent).pack(side="top", fill="both", expand=True)

    def team_frame(self, label, command):
        input_frame = ttk.Frame(self, relief="groove", width=350, height=100)
        input_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=10, ipady=10)
        ttk.Label(input_frame, text="Select a team:", justify="center") \
            .grid(row=0, column=0, padx=15, pady=5)
        team = tk.StringVar()
        teams = ("Team A", "Team B", "Team C")
        ttk.Combobox(input_frame, values=teams, state="readonly", textvariable=team) \
            .grid(row=1, column=0, padx=15, pady=5)
        team.set("Team A")
        ttk.Button(input_frame, text=label, command=lambda: command(team.get())) \
            .grid(row=2, column=0, padx=15, pady=5)


class NewProject(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Add a New Project")
        ttk.Label(self, text="Enter the release number:") \
            .grid(row=0, column=0, columnspan=5, padx=20, pady=10)
        self.entry = ttk.Entry(self, width=20)
        self.entry.grid(row=1, column=0, columnspan=5, padx=20, pady=10)
        ttk.Label(self,
                  text="Note: Make sure that all the filters for this project are set up in Jira"
                       " and that they are correctly named.",
                  wraplength=350, justify="center", foreground="grey") \
            .grid(row=2, column=0, columnspan=5, padx=20, pady=10)
        ttk.Button(self, text="Enter") \
            .grid(row=3, column=1, padx=20, pady=10)
        self.back_button.grid(row=3, column=3, padx=20, pady=10)


class UpdateSheets(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Update the Sheet")
        self.team_frame("Update", self.update_sheet)
        ttk.Label(self, text="- or -", justify="center") \
            .grid(row=1, column=0, columnspan=2)
        ttk.Button(self, text="Update All Sheets") \
            .grid(row=2, column=0, columnspan=2, padx=20, pady=15)
        self.back_button.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    def update_sheet(self, team):
        pass


class JiraIssues(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Review Jira Issues")
        self.team_frame("Find Issues", self.find_issues)
        self.new_frame = IssueFrame(self, text="New Issues")
        self.new_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, ipady=10, ipadx=10)
        self.done_frame = IssueFrame(self, text="Done Issues")
        self.done_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, ipady=10, ipadx=10)

    def find_issues(self, team):
        self.new_frame.populate()
        self.done_frame.populate()


class IssueFrame(ttk.LabelFrame):

    def __init__(self, parent, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.placeholder = ttk.Label(self, text="Select a team and click 'Find Issues'.",
                                     foreground="grey")
        self.placeholder.pack()
        self.issues = []
        self.row = 3

    def populate(self):
        for item in self.winfo_children():
            item.destroy()
        for row in range(5):
            if row < 3:
                IssueRow(self, "PC-2", "Summary" * 6).pack()
            else:
                self.issues.append(("PC-2", "New one"))
        self.config(text=f"New Issues ({len(self.issues)} more)")

    def display_issue(self):
        if self.issues:
            IssueRow(self, self.issues[0][0], self.issues[0][1]) \
                .pack()
            del self.issues[0]
            self.row += 1
            if self.issues:
                self.config(text=f"New Issues ({len(self.issues)} more)")
            else:
                self.config(text="New Issues")
        if not self.winfo_children():
            ttk.Label(self, text="No more issues for this team.", foreground="grey").pack()


class IssueRow(ttk.Frame):

    def __init__(self, parent, issue_nbr, summary, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.issue_nbr = issue_nbr
        self.link = ttk.Label(self, text=issue_nbr, foreground="blue",
                              font=('Arial', 10, 'underline'), cursor="hand2")
        self.link.grid(row=0, column=0, padx=5, pady=5)
        self.link.bind('<Button-1>', self.open_link)
        ttk.Label(self, text=summary, wraplength=250).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="Add", command=self.delete_and_add).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self, text="Ignore", command=self.delete_and_add).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self, text="Leave for Later", command=self.delete_and_add).grid(row=0, column=4, padx=5, pady=5)

    def open_link(self, event):
        webbrowser.open_new(f"https://jira-doc-tracker.atlassian.net/browse/{self.issue_nbr}")

    def delete_and_add(self):
        self.destroy()
        self.parent.display_issue()


if __name__ == "__main__":
    root = tk.Tk()
    InitialView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
