export function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <section aria-label="Preferences">
        <label>
          Email notifications
          <input type="checkbox" defaultChecked />
        </label>
      </section>
    </main>
  );
}
