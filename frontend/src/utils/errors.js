// Converte a resposta de erro do DRF em { fields: {campo: "msg"}, message: "msg geral" }.
export function parseApiError(err) {
  const response = err?.response;
  if (!response) {
    return { fields: {}, message: "Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente." };
  }
  if (response.status === 413) {
    return { fields: {}, message: "O arquivo enviado é grande demais." };
  }
  if (response.status >= 500) {
    return { fields: {}, message: "Erro no servidor. Tente novamente em alguns instantes." };
  }

  const data = response.data;
  if (!data || typeof data !== "object") {
    return { fields: {}, message: "Não foi possível concluir a operação. Tente novamente." };
  }
  if (data.detail) return { fields: {}, message: data.detail };

  const join = (value) => (Array.isArray(value) ? value.join(" ") : String(value));
  const fields = {};
  let message = "Corrija os campos destacados.";
  for (const [key, value] of Object.entries(data)) {
    // Erros que não pertencem a um campo específico viram a mensagem geral.
    if (key === "non_field_errors") message = join(value);
    else fields[key] = join(value);
  }
  return { fields, message };
}
