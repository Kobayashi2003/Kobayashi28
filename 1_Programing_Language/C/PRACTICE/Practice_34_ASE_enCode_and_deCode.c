#include <stdio.h>
#include <string.h>

typedef struct
{
    unsigned int eK[44], dK[44]; // encKey, decKey
    int Nr;                      // 10 rounds
} AesKey;

#define BLOCKSIZE 16 // AES-128分组长度为16字节

// unsigned char y[4] -> unsigned int x
#define LOAD32H(x, y)                                                                         \
    do                                                                                        \
    {                                                                                         \
        (x) = ((unsigned int)((y)[0] & 0xff) << 24) | ((unsigned int)((y)[1] & 0xff) << 16) | \
              ((unsigned int)((y)[2] & 0xff) << 8) | ((unsigned int)((y)[3] & 0xff));         \
    } while (0)

// unsigned int x -> unsigned char y[4]
#define STORE32H(x, y)                                \
    do                                                \
    {                                                 \
        (y)[0] = (unsigned char)(((x) >> 24) & 0xff); \
        (y)[1] = (unsigned char)(((x) >> 16) & 0xff); \
        (y)[2] = (unsigned char)(((x) >> 8) & 0xff);  \
        (y)[3] = (unsigned char)((x)&0xff);           \
    } while (0)

// 从uint32_t x中提取从低位开始的第n个字节
#define BYTE(x, n) (((x) >> (8 * (n))) & 0xff)

/* used for keyExpansion */
// 字节替换然后循环左移1位
#define MIX(x) (((S[BYTE(x, 2)] << 24) & 0xff000000) ^ ((S[BYTE(x, 1)] << 16) & 0xff0000) ^ \
                ((S[BYTE(x, 0)] << 8) & 0xff00) ^ (S[BYTE(x, 3)] & 0xff))

// unsigned int x循环左移n位
#define ROF32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
// unsigned int x循环右移n位
#define ROR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

/* for 128-bit blocks, Rijndael never uses more than 10 rcon values */
// AES-128轮常量
static const unsigned int rcon[10] = {
    0x01000000UL, 0x02000000UL, 0x04000000UL, 0x08000000UL, 0x10000000UL,
    0x20000000UL, 0x40000000UL, 0x80000000UL, 0x1B000000UL, 0x36000000UL};
// S盒
unsigned char S[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16};

//逆S盒
unsigned char inv_S[256] = {
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D};

/* copy in[16] to state[4][4] */
int loadStateArray(unsigned char (*state)[4], const unsigned char *in)
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[j][i] = *in++;
        }
    }
    return 0;
}

/* copy state[4][4] to out[16] */
int storeStateArray(unsigned char (*state)[4], unsigned char *out)
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            *out++ = state[j][i];
        }
    }
    return 0;
}
//秘钥扩展
int keyExpansion(const unsigned char *key, unsigned int keyLen, AesKey *aesKey)
{

    if (NULL == key || NULL == aesKey)
    {
        printf("keyExpansion param is NULL\n");
        return -1;
    }

    if (keyLen != 16)
    {
        printf("keyExpansion keyLen = %d, Not support.\n", keyLen);
        return -1;
    }

    unsigned int *w = aesKey->eK; //加密秘钥
    unsigned int *v = aesKey->dK; //解密秘钥

    /* keyLen is 16 Bytes, generate unsigned int W[44]. */

    /* W[0-3] */
    for (int i = 0; i < 4; ++i)
    {
        LOAD32H(w[i], key + 4 * i);
    }

    /* W[4-43] */
    for (int i = 0; i < 10; ++i)
    {
        w[4] = w[0] ^ MIX(w[3]) ^ rcon[i];
        w[5] = w[1] ^ w[4];
        w[6] = w[2] ^ w[5];
        w[7] = w[3] ^ w[6];
        w += 4;
    }

    w = aesKey->eK + 44 - 4;
    //解密秘钥矩阵为加密秘钥矩阵的倒序，方便使用，把ek的11个矩阵倒序排列分配给dk作为解密秘钥
    //即dk[0-3]=ek[41-44], dk[4-7]=ek[37-40]... dk[41-44]=ek[0-3]
    for (int j = 0; j < 11; ++j)
    {

        for (int i = 0; i < 4; ++i)
        {
            v[i] = w[i];
        }
        w -= 4;
        v += 4;
    }

    return 0;
}

// 轮秘钥加
int addRoundKey(unsigned char (*state)[4], const unsigned int *key)
{
    unsigned char k[4][4];

    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            k[i][j] = (unsigned char)BYTE(key[j], 3 - i); /* 把 uint32 key[4] 先转换为矩阵 uint8 k[4][4] */
            state[i][j] ^= k[i][j];
        }
    }

    return 0;
}

//字节替换
int subBytes(unsigned char (*state)[4])
{
    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = S[state[i][j]]; //直接使用原始字节作为S盒数据下标
        }
    }

    return 0;
}

//逆字节替换
int invSubBytes(unsigned char (*state)[4])
{
    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = inv_S[state[i][j]];
        }
    }
    return 0;
}

//行移位
int shiftRows(unsigned char (*state)[4])
{
    unsigned int block[4] = {0};

    /* i: row */
    for (int i = 0; i < 4; ++i)
    {
        //便于行循环移位，先把一行4字节拼成uint_32结构，移位后再转成独立的4个字节uint8_t
        LOAD32H(block[i], state[i]);
        block[i] = ROF32(block[i], 8 * i);
        STORE32H(block[i], state[i]);
    }

    return 0;
}

//逆行移位
int invShiftRows(unsigned char (*state)[4])
{
    unsigned int block[4] = {0};

    /* i: row */
    for (int i = 0; i < 4; ++i)
    {
        LOAD32H(block[i], state[i]);
        block[i] = ROR32(block[i], 8 * i);
        STORE32H(block[i], state[i]);
    }

    return 0;
}

/* Galois Field (256) Multiplication of two Bytes */
// 两字节的伽罗华域乘法运算
unsigned char GMul(unsigned char u, unsigned char v)
{
    unsigned char p = 0;

    for (int i = 0; i < 8; ++i)
    {
        if (u & 0x01)
        { //
            p ^= v;
        }

        int flag = (v & 0x80);
        v <<= 1;
        if (flag)
        {
            v ^= 0x1B; /* x^8 + x^4 + x^3 + x + 1 */
        }

        u >>= 1;
    }

    return p;
}

// 列混合
int mixColumns(unsigned char (*state)[4])
{
    unsigned char tmp[4][4];
    unsigned char M[4][4] = {{0x02, 0x03, 0x01, 0x01},
                             {0x01, 0x02, 0x03, 0x01},
                             {0x01, 0x01, 0x02, 0x03},
                             {0x03, 0x01, 0x01, 0x02}};

    /* copy state[4][4] to tmp[4][4] */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            tmp[i][j] = state[i][j];
        }
    }

    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        { //伽罗华域加法和乘法
            state[i][j] = GMul(M[i][0], tmp[0][j]) ^ GMul(M[i][1], tmp[1][j]) ^ GMul(M[i][2], tmp[2][j]) ^ GMul(M[i][3], tmp[3][j]);
        }
    }

    return 0;
}

// 逆列混合
int invMixColumns(unsigned char (*state)[4])
{
    unsigned char tmp[4][4];
    unsigned char M[4][4] = {{0x0E, 0x0B, 0x0D, 0x09},
                             {0x09, 0x0E, 0x0B, 0x0D},
                             {0x0D, 0x09, 0x0E, 0x0B},
                             {0x0B, 0x0D, 0x09, 0x0E}}; //使用列混合矩阵的逆矩阵

    /* copy state[4][4] to tmp[4][4] */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            tmp[i][j] = state[i][j];
        }
    }

    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = GMul(M[i][0], tmp[0][j]) ^ GMul(M[i][1], tmp[1][j]) ^ GMul(M[i][2], tmp[2][j]) ^ GMul(M[i][3], tmp[3][j]);
        }
    }

    return 0;
}

// AES-128加密接口，输入key应为16字节长度，输入长度应该是16字节整倍数，
// 这样输出长度与输入长度相同，函数调用外部为输出数据分配内存
int aesEncrypt(const unsigned char *key, unsigned int keyLen, const unsigned char *pt, unsigned char *ct, unsigned int len)
{

    AesKey aesKey;
    unsigned char *pos = ct;
    const unsigned int *rk = aesKey.eK; //解密秘钥指针
    unsigned char out[BLOCKSIZE] = {0};
    unsigned char actualKey[16] = {0};
    unsigned char state[4][4] = {0};

    if (NULL == key || NULL == pt || NULL == ct)
    {
        printf("param err.\n");
        return -1;
    }

    if (keyLen > 16)
    {
        printf("keyLen must be 16.\n");
        return -1;
    }

    if (len % BLOCKSIZE)
    {
        printf("inLen is invalid.\n");
        return -1;
    }

    memcpy(actualKey, key, keyLen);
    keyExpansion(actualKey, 16, &aesKey); // 秘钥扩展

    // 使用ECB模式循环加密多个分组长度的数据
    for (int i = 0; (unsigned)i < len; i += BLOCKSIZE)
    {
        // 把16字节的明文转换为4x4状态矩阵来进行处理
        loadStateArray(state, pt);
        // 轮秘钥加
        addRoundKey(state, rk);

        for (int j = 1; j < 10; ++j)
        {
            rk += 4;
            subBytes(state);        // 字节替换
            shiftRows(state);       // 行移位
            mixColumns(state);      // 列混合
            addRoundKey(state, rk); // 轮秘钥加
        }

        subBytes(state);  // 字节替换
        shiftRows(state); // 行移位
        // 此处不进行列混合
        addRoundKey(state, rk + 4); // 轮秘钥加

        // 把4x4状态矩阵转换为uint8_t一维数组输出保存
        storeStateArray(state, pos);

        pos += BLOCKSIZE; // 加密数据内存指针移动到下一个分组
        pt += BLOCKSIZE;  // 明文数据指针移动到下一个分组
        rk = aesKey.eK;   // 恢复rk指针到秘钥初始位置
    }
    return 0;
}

// AES128解密， 参数要求同加密
int aesDecrypt(const unsigned char *key, unsigned int keyLen, const unsigned char *ct, unsigned char *pt, unsigned int len)
{
    AesKey aesKey;
    unsigned char *pos = pt;
    const unsigned int *rk = aesKey.dK; //解密秘钥指针
    unsigned char out[BLOCKSIZE] = {0};
    unsigned char actualKey[16] = {0};
    unsigned char state[4][4] = {0};

    if (NULL == key || NULL == ct || NULL == pt)
    {
        printf("param err.\n");
        return -1;
    }

    if (keyLen > 16)
    {
        printf("keyLen must be 16.\n");
        return -1;
    }

    if (len % BLOCKSIZE)
    {
        printf("inLen is invalid.\n");
        return -1;
    }

    memcpy(actualKey, key, keyLen);
    keyExpansion(actualKey, 16, &aesKey); //秘钥扩展，同加密

    for (int i = 0; (unsigned)i < len; i += BLOCKSIZE)
    {
        // 把16字节的密文转换为4x4状态矩阵来进行处理
        loadStateArray(state, ct);
        // 轮秘钥加，同加密
        addRoundKey(state, rk);

        for (int j = 1; j < 10; ++j)
        {
            rk += 4;
            invShiftRows(state);    // 逆行移位
            invSubBytes(state);     // 逆字节替换，这两步顺序可以颠倒
            addRoundKey(state, rk); // 轮秘钥加，同加密
            invMixColumns(state);   // 逆列混合
        }

        invSubBytes(state);  // 逆字节替换
        invShiftRows(state); // 逆行移位
        // 此处没有逆列混合
        addRoundKey(state, rk + 4); // 轮秘钥加，同加密

        storeStateArray(state, pos); // 保存明文数据
        pos += BLOCKSIZE;            // 输出数据内存指针移位分组长度
        ct += BLOCKSIZE;             // 输入数据内存指针移位分组长度
        rk = aesKey.dK;              // 恢复rk指针到秘钥初始位置
    }
    return 0;
}

// 方便输出16进制数据
void printHex(const unsigned char *ptr, int len, const char *tag)
{
    printf("%s\ndata[%d]: ", tag, len);
    for (int i = 0; i < len; ++i)
    {
        printf("%.2X ", *ptr++);
    }
    printf("\n");
}

int main()
{

    // case 1
    const unsigned char key[16] = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};
    const unsigned char pt[16] = {0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34};
    unsigned char ct[16] = {0};    // 外部申请输出数据内存，用于加密后的数据
    unsigned char plain[16] = {0}; // 外部申请输出数据内存，用于解密后的数据

    aesEncrypt(key, 16, pt, ct, 16);                                             // 加密
    printHex(pt, 16, "plain data:");                                             // 打印初始明文数据
    printf("expect cipher:\n39 25 84 1D 02 DC 09 FB DC 11 85 97 19 6A 0B 32\n"); // 正常解密后的数据内容

    printHex(ct, 16, "after encryption:"); // 打印加密后的密文

    aesDecrypt(key, 16, ct, plain, 16);       // 解密
    printHex(plain, 16, "after decryption:"); // 打印解密后的明文数据

    // case 2
    // 16字节字符串形式秘钥
    const unsigned char key2[] = "1234567890123456";
    // 32字节长度字符串明文
    const unsigned char *data = (unsigned char *)"abcdefghijklmnopqrstuvwxyz123456";
    unsigned char ct2[32] = {0};    //外部申请输出数据内存，用于存放加密后数据
    unsigned char plain2[32] = {0}; //外部申请输出数据内存，用于存放解密后数据
    //加密32字节明文
    aesEncrypt(key2, 16, data, ct2, 32);

    printf("\nplain text:\n%s\n", data);
    printf("expect ciphertext:\nfcad715bd73b5cb0488f840f3bad7889\n");
    printHex(ct2, 32, "after encryption:");

    // 解密32字节密文
    aesDecrypt(key2, 16, ct2, plain2, 32);
    // 打印16进制形式的解密后的明文
    printHex(plain2, 32, "after decryption:");

    // 因为加密前的数据为可见字符的字符串，打印解密后的明文字符，与加密前明文进行对比
    printf("output plain text\n");
    for (int i = 0; i < 32; ++i)
    {
        printf("%c ", plain2[i]);
    }

    return 0;
}