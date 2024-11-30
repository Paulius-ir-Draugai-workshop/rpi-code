#include "dll.h"
#include "string.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PRINTF printf

Dll dll;

void dllInit(uint8_t type) {
  dll.state = DLL_NSYNC;
  dll.dataCount = 0;
  dll.dllIndex = 0;
  dll.count = 0;
  dll.sof = 0;
  dll.dataReceiveIndex = 0;
  dll.escFlag = 0;
  dll.type = type;
  memset(dll.dataBuffer, 0, sizeof(dll.dataBuffer) / sizeof(dll.dataBuffer[0]));
  memset(dll.dllBuffer, 0, sizeof(dll.dllBuffer) / sizeof(dll.dllBuffer[0]));
}

void dllPack(uint8_t *inputBuffer, int16_t size) {
  uint16_t i;
  uint16_t count = 0;

  dll.dllBuffer[count++] = 'S';

  for (i = 0; i < size; i++) {
    if (dll.type == DLL_VER_1) {
      if (inputBuffer[i] == 'S' || inputBuffer[i] == '/') {
        dll.dllBuffer[count++] = '/';
        dll.dllBuffer[count++] = inputBuffer[i];
      } else
        dll.dllBuffer[count++] = inputBuffer[i];
    } else {
      if ((inputBuffer[i] == 'S') || (inputBuffer[i] == 'E') ||
          (inputBuffer[i] == '/')) {
        dll.dllBuffer[count++] = '/';
        dll.dllBuffer[count++] = inputBuffer[i];
      } else
        dll.dllBuffer[count++] = inputBuffer[i];
    }
  }
  if (dll.type == DLL_VER_2)
    dll.dllBuffer[count++] = 'E'; // Add a trailing S in ver-2
  dll.count = count;
}

void dllRcv(char c) {

  if (dll.dataReceiveIndex == MAILBOX_SIZE) {
    PRINTF("ERROR: rx buffer (size %d) overflow, dropping frame and resyncing "
           "DLL\n",
           MAILBOX_SIZE);
    dll.state = DLL_NSYNC;
  }

  switch (dll.state) {
  case DLL_NSYNC:
    if (c == 'S') {
      dll.state = DLL_SYNC;
      dll.dataReceiveIndex = 0;
      dll.dataCount = 0;
      dll.escFlag = 0;
    } else {
      // discard ruthlessly anything received before a synced dll;
      // ie, no need to track or update escOn until dll is synced
      PRINTF("NSYNC %02x\n", c);
    }
    break;

  case DLL_SYNC:
    if (c == 'S') {
      if (dll.escFlag) {
        dll.escFlag = 0;
        // S is part of the frame
        dll.dataBuffer[dll.dataReceiveIndex++] = c;
      } else {
        // start of frame
        dll.dataReceiveIndex = 0;
        dll.dataCount = 0;
        dll.escFlag = 0;
      }
    } else if (c == 'E') {
      if (dll.escFlag) {
        dll.escFlag = 0;
        // E is part of the frame
        dll.dataBuffer[dll.dataReceiveIndex++] = c;
      } else {
        // end of frame
        dll.dataCount = dll.dataReceiveIndex;
      }
    } else if (c == '/') {
      if (dll.escFlag)
        dll.dataBuffer[dll.dataReceiveIndex++] = c;
      dll.escFlag = !dll.escFlag;
    } else { // non-special char
      if (dll.escFlag) {
        PRINTF("ERROR: got malformed data (%02x), resyncing DLL\n", c);
        dll.state = DLL_NSYNC;
        dll.dataReceiveIndex = 0;
        dll.escFlag = 0;
      } else
        dll.dataBuffer[dll.dataReceiveIndex++] = c;
    }
    break;

  default:
    PRINTF("ERROR: DLL in illegal state (%d)\n", dll.state);
    break;
  }
}

// int main() {
//   dllInit(DLL_VER_2);
//   uint8_t input[10] = {'a', 'b', '/', 'S', 'e', 'f', 'g', 'h', 'i', 'j'};
//   uint8_t output[20];

//   // print the actual input from application layer
//   printf("Input is :");
//   for (int i = 0; i < 10; i++)
//     printf("%c", input[i]);
//   printf("\n");

//   // Serialize the input from the application layer by framing it
//   dllPack(input, 10);

//   // print the serialized input data
//   printf("Serialized data is :");
//   for (int i = 0; i < dll.count; i++) {
//     printf("%c", dll.dllBuffer[i]);
//   }
//   printf("\n");

//   // Receive the serialized data byte by byte in order to deserialize it
//   for (int i = 0; i < dll.count; i++)
//     dllRcv(dll.dllBuffer[i]); // Plays role of receiver

//   if (dll.dataCount) { // If we have a valid frame, save data in output
//   buffer
//     and print it printf("Output is :");
//     for (int j = 0; j < dll.dataCount; j++) {
//       output[j] = dll.dataBuffer[j];
//       printf("%c", output[j]);
//     }
//     printf("\n");
//   }
// }
