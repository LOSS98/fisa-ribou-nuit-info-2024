export interface Question {
    id: number;
    question: string;
    answer: "L'Humain" | "L'Océan" | "Les deux";  // Only these three possible answers
}

export interface GameState {
    currentQuestion: number;
    streak: number;
    gameOver: boolean;
}