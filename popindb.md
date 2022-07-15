# Idea
Build up PopIn as a super slick looking forum.
This way, events need not be modeled as a collection of complex interactions between users
but instead as a collection of users interacting with events themselves. The data heirarchy
would be thus:

PopIn: _____ { \
    * Locale: {\
        * Events: { \
        * People associated with event \
        * Messages \
        * Media associated with event \
        } \
        } \
        }
        
