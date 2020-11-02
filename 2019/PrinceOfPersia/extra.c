#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define N1 256

// data:23E0
const char block1[] = {214, 85, 173,9, 13, 217,126, 133, 241,98, 37, 11,50, 52, 8,18, 230, 22,122, 125, 160,86, 8, 226,17, 235, 234,154, 238, 250,210, 123, 171,178, 43, 98,237, 136, 68,184, 17, 74,113, 74, 138};


// data:4281
char rooms[15] = {9, 23, 6, 24, 18, 22, 3, 3, 5, 8, 24, 23, 3, 23, 3};
char tbl_seamless_exit[16] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1};
char pre[] = {0x26, 0x10, 0x06, 0x04, 0x12, 0x5d};
void swap(unsigned char *a, unsigned char *b);
int KSA(char *key, unsigned char *S);
int PRGA(unsigned char *S, char *plaintext, unsigned char *ciphertext);
void decode(char* arr, char* res, int len);
int RC(char *key, char *plaintext, unsigned char *ciphertext);

void SOLVE();
int current_level=14; // with this value we use all of 'block1'

int main(int argc, char**argv)
{
	SOLVE();
	return 0;
}

void SOLVE()
{
	char strrc[100] = { 0 };
	char arr[8] = { 0 };
	char finalstr[100] = { 0 };
	char str[57] = {0};
    rooms[12 - 1] = tbl_seamless_exit[12];
	rooms[current_level - 1] = 20;
	for (int i = 0, j = 0; i < (current_level + 1) * 4; i++) {
		if (i % 4 != 3) {
			str[j*3 + i % 4] = block1[i-j];
		}
		else {
			j++;
		}
	}
	RC(rooms, str, (unsigned char*)strrc);
	decode(pre, arr,5);
	sprintf(finalstr,"%s\n%s", arr, strrc);
	printf("%s\n", finalstr);
    //printf("%s\n", arr);
    //printf("%s\n", strrc);
}

void swap(unsigned char *a, unsigned char *b) {
	unsigned char tmp = *a;
	*a = *b;
	*b = tmp;
}

int KSA(char *key, unsigned char *S) {
	int len = 15;
	int j = 0;
	for (int i = 0; i < N1; i++)
		S[i] = i;
	for (int i = 0; i < N1; i++) {
		j = (j + S[i] + key[i % len]) % N1;
		swap(&S[i], &S[j]);
	}
	return 0;
}

// seg005:04EB
int RC(char *key, char *plaintext, unsigned char *ciphertext) {

	unsigned char S[N1];
	KSA(key, S);

	PRGA(S, plaintext, ciphertext);

	return 0;
}

// seg007:0632
int PRGA(unsigned char *S, char *plaintext, unsigned char *ciphertext) {
	int i = 0;
	int j = 0;
	for (size_t n = 0, len = strlen(plaintext); n < len; n++) {
		i = (i + 1) % N1;
		j = (j + S[i]) % N1;
		swap(&S[i], &S[j]);
		int rnd = S[(S[i] + S[j]) % N1];
		ciphertext[n] = rnd ^ plaintext[n];
	}
	return 0;
}

// seg007:9ADC
void decode(char* arr, char* res, int len) {
	res[0] = arr[0] ^ 0x61;
	res[1] = arr[1] ^ 0x62;
	res[2] = arr[2] ^ 0x63;
	res[3] = arr[3] ^ 0x65;
	res[4] = arr[4] ^ 0x66;
	res[5] = arr[5] ^ 0x67;
}
