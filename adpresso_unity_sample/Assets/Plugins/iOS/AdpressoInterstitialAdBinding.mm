//
//  AdpressoInterstitialAdBinding.mm
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//
#import "AdpressoInterstitialAdBinding.h"

// void UnitySendMessage(const char* obj, const char* method, const char* msg);

@implementation AdpressoInterstitialAdListenerBinding

//
// turn src to a cstring, then copy it into dst
//
-(BOOL)NSStringToCString:(NSString*)src dst:(char **)dst
{
    if( src == NULL ) return NO;
    if( (*dst = (char *)malloc([src length])) == NULL ) return NO;
    
    strcpy(*dst, [src UTF8String]);
    
    return YES;
}

-(id)initWithName:(NSString *)callbackObjectName
{
    if ( self = [super init] ) {
        if (callbackObjectName != NULL ) {
            // [NSString UTF8String] will free the memory automatically.
            // we have to copy the string into unityCallbackObjectName
            [self NSStringToCString:callbackObjectName dst:&unityCallbackObjectName];
        }
    }
    
    return self;
}
- (void)interstitialAdRequestComplete:(AdpressoInterstitialAd*)interstitialAd
{
    if (unityCallbackObjectName != NULL) {
        UnitySendMessage(unityCallbackObjectName, "interstitialAdRequestComplete", "");
    }
}

- (void)interstitialAdRequestFailed:(AdpressoInterstitialAd*)interstitialAd
{
    if (unityCallbackObjectName != NULL) {
        UnitySendMessage(unityCallbackObjectName, "interstitialAdRequestFailed", "");
    }
}


- (void)interstitialAdWillBePresented:(AdpressoInterstitialAd*)interstitialAd
{
    if (unityCallbackObjectName != NULL) {
        UnitySendMessage(unityCallbackObjectName, "interstitialAdWillBePresented", "");
    }
}


- (void)interstitialAdWasDismissed:(AdpressoInterstitialAd*)interstitialAd
{
    if (unityCallbackObjectName != NULL) {
        UnitySendMessage(unityCallbackObjectName, "interstitialAdWasDismissed", "");
    }
}

@end

static AdpressoInterstitialAd * gAdpressoInterstitialAd = nil;
static AdpressoInterstitialAdListenerBinding *gAdpressoInterstitialAdListener = nil;

void _AdpressoIntersitial_Init(char * inPublisherId, char *callbackObjectName)
{
  if (gAdpressoInterstitialAd == nil) {
    gAdpressoInterstitialAd = [AdpressoInterstitialAd interstitialAdWithPublisherId:@(inPublisherId)];
    gAdpressoInterstitialAdListener = [[AdpressoInterstitialAdListenerBinding alloc] initWithName:@(callbackObjectName)];
    gAdpressoInterstitialAd.delegate = gAdpressoInterstitialAdListener;
  }
}

void _AdpressoIntersitial_Show()
{
  [gAdpressoInterstitialAd show];
}
void _AdpressoIntersitial_Cancel()
{
  [gAdpressoInterstitialAd cancel];
}
