//========= Copyright 2018, HTC Corporation. All rights reserved. ===========
namespace Vive
{
    namespace Plugin.SR
    {

        /** @enum ModuleType
        An enum type of SRWorks engine. used for Vive.Plugin.SR.SRWorkModule_API.Initial().
        */
        public enum ModuleType
        {
            SEETHROUGH = 0,
            DEPTH,
            DEPTHMESH,
            RIGIDRECONSTRUCTION,
            SEETHROUGH4K,
            CONTROLLER_POSE,
            MAX,
        }
        /** @enum ModuleStatus
        An enum type of modules status.
        */
        public enum ModuleStatus
        {
            ERROR,
            IDLE,
            WORKING,
        }
    }
}