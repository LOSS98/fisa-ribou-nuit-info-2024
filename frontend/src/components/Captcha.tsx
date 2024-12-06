import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
    Bot,
    Brain,
    Heart,
    Droplets,
    Ship,
    Users
} from 'lucide-react';

interface MemoryCard {
    id: number;
    value: number;
    icon: React.ReactNode;
    category: string;
    isFlipped: boolean;
    isMatched: boolean;
}

interface CaptchaProps {
    onVerify: (verified: boolean) => void;
}

const CARD_ICONS = [
    { value: 1, icon: <Brain className="w-8 h-8 text-white" />, category: 'human', bg: 'bg-pink-500' },
    { value: 2, icon: <Heart className="w-8 h-8 text-white" />, category: 'human', bg: 'bg-red-500' },
    { value: 3, icon: <Ship className="w-8 h-8 text-white" />, category: 'ocean', bg: 'bg-blue-500' },
    { value: 4, icon: <Droplets className="w-8 h-8 text-white" />, category: 'ocean', bg: 'bg-cyan-500' },
    { value: 5, icon: <Users className="w-8 h-8 text-white" />, category: 'both', bg: 'bg-purple-500' },
];

export const MemoryCaptcha: React.FC<CaptchaProps> = ({ onVerify }) => {
    const [showGame, setShowGame] = useState(false);
    const [cards, setCards] = useState<MemoryCard[]>([]);
    const [flippedCards, setFlippedCards] = useState<number[]>([]);
    const [isVerified, setIsVerified] = useState(false);
    const [isChecking, setIsChecking] = useState(false);

    useEffect(() => {
        if (showGame) {
            const values = [1, 1, 2, 2, 3, 3, 4, 4, 5];
            const shuffledCards: {
                isMatched: boolean;
                icon: React.JSX.Element;
                id: number;
                category: string;
                isFlipped: boolean;
                value: number
            }[] = values
                .sort(() => Math.random() - 0.5)
                .map((value, index) => {
                    const iconData = CARD_ICONS[value - 1];
                    return {
                        id: index,
                        value,
                        icon: iconData.icon,
                        category: iconData.category,
                        isFlipped: false,
                        isMatched: false,
                    };
                });
            setCards(shuffledCards);
            setFlippedCards([]);
            setIsVerified(false);
            onVerify(false);
        }
    }, [onVerify, showGame]);

    const handleCardClick = async (cardId: number) => {
        if (isChecking ||
            cards[cardId].isMatched ||
            flippedCards.includes(cardId) ||
            flippedCards.length === 2) return;

        setCards(cards.map(card =>
            card.id === cardId ? { ...card, isFlipped: true } : card
        ));

        const newFlippedCards = [...flippedCards, cardId];
        setFlippedCards(newFlippedCards);

        if (newFlippedCards.length === 2) {
            const [firstId, secondId] = newFlippedCards;
            const firstCard = cards[firstId];
            const secondCard = cards[secondId];

            setIsChecking(true);

            await new Promise(resolve => setTimeout(resolve, 1000));

            if (firstCard.value === secondCard.value) {
                setCards(cards.map(card =>
                    card.id === firstId || card.id === secondId
                        ? { ...card, isMatched: true, isFlipped: true }
                        : card
                ));
            } else {
                setCards(cards.map(card =>
                    card.id === firstId || card.id === secondId
                        ? { ...card, isFlipped: false }
                        : card
                ));
            }

            setFlippedCards([]);
            setIsChecking(false);
        }
    };

    useEffect(() => {
        if (cards.length > 0) {
            const pairedCards = cards.filter(card => card.value !== 5);
            const allPairsMatched = pairedCards.every(card => card.isMatched);

            if (allPairsMatched) {
                setIsVerified(true);
                onVerify(true);
                setTimeout(() => {
                    setShowGame(false);
                }, 1000);
            }
        }
    }, [cards, onVerify]);

    const getCardBackground = (card: MemoryCard) => {
        if (!card.isFlipped) return 'bg-slate-700';
        return CARD_ICONS[card.value - 1].bg;
    };

    return (
        <div>
            <Button
                onClick={() => setShowGame(true)}
                className="w-full mb-4"
                disabled={isVerified}
            >
                {isVerified ? "Verified ✓" : "Verify you're not a robot"}
                {!isVerified && <Bot className="ml-2 h-4 w-4" />}
            </Button>

            <Dialog open={showGame} onOpenChange={setShowGame}>
                <DialogContent className="sm:max-w-[425px] [&>button]:hidden">
                    <div className="grid grid-cols-3 gap-4 p-4">
                        {cards.map((card) => (
                            <Card
                                key={card.id}
                                className={`
                  h-24 cursor-pointer transition-all duration-300 transform
                  ${getCardBackground(card)}
                  ${card.isMatched ? 'opacity-70 cursor-not-allowed' : ''}
                  ${isChecking ? 'pointer-events-none' : 'hover:scale-105'}
                  flex items-center justify-center
                `}
                                onClick={() => handleCardClick(card.id)}
                            >
                                {card.isFlipped && card.icon}
                            </Card>
                        ))}
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
};