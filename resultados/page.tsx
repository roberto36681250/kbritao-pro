"use client";
import { useEffect, useState } from "react";

export default function Page() {
  const [resultado, setResultado] = useState(null);

  useEffect(() => {
    const data = localStorage.getItem("resultado");
    if (data) setResultado(JSON.parse(data));
  }, []);

  if (!resultado) return <p className="p-6">Nenhum resultado encontrado.</p>;

  return (
    <main className="p-6 space-y-2">
      <h2 className="text-xl font-bold text-green-800">📋 Resultado da Simulação</h2>
      {Object.entries(resultado.detalhes).map(([key, val]) => (
        <p key={key}>✅ {key}: R$ {parseFloat(val).toFixed(2)}</p>
      ))}
      <p className="font-bold mt-4">💰 Frete sugerido: R$ {resultado.freteFinal}</p>
    </main>
  )
}