import React, { useEffect, useState, useRef } from "react";

const RandomAsciiLogo: React.FC = () => {
    const [position, setPosition] = useState<{ top: string; left: string }>({
        top: "50%",
        left: "50%",
    });

    const logoRef = useRef<HTMLDivElement | null>(null);

    const handleClick = () => {
        // Ouvre une nouvelle page vierge si on clique sur le logo
        window.open("about:blank", "_blank");
    };

    useEffect(() => {
        // Générer une position initiale aléatoire
        const randomTop = Math.floor(Math.random() * 80) + "%";
        const randomLeft = Math.floor(Math.random() * 80) + "%";
        setPosition({ top: randomTop, left: randomLeft });
    }, []); // Exécuté une seule fois lors du chargement du composant

    return (
        <div
            ref={logoRef}
            onClick={handleClick} // Détecte le clic sur le logo
            className="absolute text-white font-mono"
            style={{
                top: position.top,
                left: position.left,
                transform: "translate(-50%, -50%) scale(0.1)", // Réduit l'échelle
                opacity: 0.2, // Réduire l'opacité pour un aspect discret
                whiteSpace: "pre", // Maintenir le formatage ASCII
                fontSize: "8px", // Taille réduite du texte
                pointerEvents: "auto", // Permet au logo de détecter les clics
                cursor: "default", // Curseur par défaut
                userSelect: "none", // Empêche la sélection de texte
            }}
        >
      <pre>{`   ...........::---:.....................................................................   
   .......:----:.........................................................................   
   ...:-----:.-===-......................................................................   
   .:-----:...+###+......................................................................   
   .----:.....+###+..:====:.....:=---==-..-+-...-+***=......:=****++-...:=****+:.........   
   .:--:......+###+...-####-...-##--####*###+:+###=-*##*:.-####=--=*#.=####==*###=.......   
   ..::.......+###*....:####:.-##:.-####-...:=###=.:-###=-####-......:####:...####=..:-..   
   ...........+###+.....:*###=##-..-###*:....+###*++++++-=####-......-####....*###=::+*=:   
   ...........+###*.......+####-...-###*:....-####-.......*###*:.....:####-..-####-.+***+   
   ...........+##########:=###-....-###*:.....:=########=..-*#######*.:=*#######=:-****+:   
   ......................:*##:..................................................-****+-..   
   .....................:*##:................................................:+***+-:....   
   .....................................................................:-=**+=:.........   
   ................................................................:-++=:::..............   
   .......................................................::::--::.......................`}</pre>
        </div>
    );
};

export const AsciiLogo: React.FC = () => {
    return (
        <div className="relative flex h-screen w-screen bg-black"> {/* Fond noir ajouté */}
            {/* Intégrer le logo ASCII */}
            <RandomAsciiLogo />
        </div>
    );
};