#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

struct GameState {
    char buffer[32];
    int samurai_hp;
};

void fight_phase1() {
    struct GameState state;
    state.samurai_hp = 999;
    
    printf("PHASE|1\n");
    printf("HP|%d\n", state.samurai_hp);
    printf("MSG|You dare approach me? My armor is impenetrable.\n");
    printf("PROMPT|Enter your battle cry to break his guard\n");
    
    gets(state.buffer); 
    
    if (state.samurai_hp <= 0) {
        printf("TRANSITION|\n");
    } else {
        printf("MSG|Pathetic. Your words mean nothing.\n");
        printf("DIE|\n");
        exit(0);
    }
}

void fight_phase2() {
    int samurai_hp = INT_MAX;
    int choice, item, target, amount;
    
    while(1) {
        printf("PHASE|2\n");
        printf("HP|%d\n", samurai_hp);
        printf("MSG|I HAVE SHED MY MORTAL SHELL. I AM THE VOID.\n");
        printf("PROMPT|[1] Strike  [2] Defend  [3] Use Item\n");
        
        if (scanf("%d", &choice) != 1) exit(0);
        
        if (choice == 1) {
            printf("MSG|Your blade passes through him like mist. He strikes back!\n");
            printf("DIE|\n");
            exit(0);
        } else if (choice == 2) {
            printf("MSG|You brace yourself. He stares into your soul.\n");
        } else if (choice == 3) {
            printf("PROMPT|Select Item  [1] Health Potion  [2] Smoke Bomb\n");
            scanf("%d", &item);
            if (item == 1) {
                printf("PROMPT|Select Target  [1] Self  [2] The Beast\n");
                scanf("%d", &target);
                if (target == 2) {
                    printf("PROMPT|How many drops to pour?\n");
                    scanf("%d", &amount);
                    if (amount <= 0) {
                        printf("MSG|You hesitate. He strikes!\n");
                        printf("DIE|\n");
                        exit(0);
                    }
                    
                    samurai_hp += amount;
                    
                    if (samurai_hp == INT_MIN) {
                        printf("WIN|\n");
    FILE *f = fopen("flag.txt", "r");
    if (f != NULL) {
        char flag[100];
        fgets(flag, sizeof(flag), f);
        printf("FLAG|%s\n", flag);
        fclose(f);
    } else {
        printf("FLAG|Error reading flag.txt\n");
    }
                        exit(0);
                    } else if (samurai_hp < 0) {
                        printf("MSG|An imperfect overflow tears the fabric of reality. You both perish.\n");
                        printf("DIE|\n");
                        exit(0);
                    } else {
                        printf("MSG|He absorbs the life force. HP is now %d. You fool.\n", samurai_hp);
                        printf("DIE|\n");
                        exit(0);
                    }
                } else {
                    printf("MSG|You drink it but your despair remains. He strikes!\n");
                    printf("DIE|\n");
                    exit(0);
                }
            } else {
                printf("MSG|The smoke does nothing against the void.\n");
                printf("DIE|\n");
                exit(0);
            }
        } else {
            printf("MSG|You stumble in fear. He strikes!\n");
            printf("DIE|\n");
            exit(0);
        }
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    fight_phase1();
    fight_phase2();
    return 0;
}
