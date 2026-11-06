<template>
    <nav class="tabs" aria-label="Acesso à conta">
        <RouterLink to="/login" class="tab">Entrar</RouterLink>
        <RouterLink to="/cadastro" class="tab">Criar conta</RouterLink>
    </nav>
</template>

<style scoped>
.tabs {
    display: flex;
    gap: 4px;
    padding: 4px;
    margin-bottom: 16px;
    background: #eceef2;
    border-radius: 12px;
}

.tab {
    flex: 1;
    text-align: center;
    padding: 10px 12px;
    border-radius: 9px;
    font-weight: 600;
    color: var(--muted);
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}

.tab:hover {
    color: var(--text);
}

.tab.router-link-active {
    background: #fff;
    color: var(--text);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.tab:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
</style>