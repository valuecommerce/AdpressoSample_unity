//
//  AdpressoInterstitialAdBinding.h
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//

#ifdef __cplusplus
extern "C" {
#endif
  
#import <Foundation/Foundation.h>
#import "AdpressoInterstitialAd.h"
  
  @interface AdpressoInterstitialAdListenerBinding : NSObject <AdlantisInterstitialAdDelegate>
{
  char* unityCallbackObjectName;
}

-(id)initWithName:(NSString *)callbackObjectName;

@end
  
  void _AdpressoIntersitial_Init(char * inPublisherId, char *callbackObjectName);
  void _AdpressoIntersitial_Show();
  void _AdpressoIntersitial_Cancel();
  
#ifdef __cplusplus
}
#endif
