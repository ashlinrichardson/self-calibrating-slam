//
// Created by art on 23-03-21.
//

#include "types_sclam2d.h"

#include "g2o/core/factory.h"

namespace g2o {
    G2O_REGISTER_TYPE_GROUP(scslam2d);

    G2O_REGISTER_TYPE(NODE_V2, NodeV2);
    G2O_REGISTER_TYPE(NODE_SE2, NodeSE2);
    G2O_REGISTER_TYPE(PARAM_V2, ParamV2);
    G2O_REGISTER_TYPE(PARAM_SE2, ParamSE2);
    G2O_REGISTER_TYPE(INFO3, Info3);

    G2O_REGISTER_TYPE(CONSTRAINT_POSE2D_SE2, ConstraintPose2DSE2);
    G2O_REGISTER_TYPE(CONSTRAINT_POSE2D_V2, ConstraintPose2DV2);
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2, ConstraintPoses2DSE2);
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_PV2, ConstraintPoses2DSE2PV2);
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_PSE2, ConstraintPoses2DSE2PSE2);
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_COV, ConstraintPoses2DSE2Cov);
}