/******************************************************************************
*                 SOFA, Simulation Open-Framework Architecture                *
*                    (c) 2006 INRIA, USTL, UJF, CNRS, MGH                     *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU General Public License as published by the Free  *
* Software Foundation; either version 2 of the License, or (at your option)   *
* any later version.                                                          *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    *
* more details.                                                               *
*                                                                             *
* You should have received a copy of the GNU General Public License along     *
* with this program. If not, see <http://www.gnu.org/licenses/>.              *
*******************************************************************************
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/

//#define MAPPEDSTATEOBSERVATIONMANAGER_CPP

#include <sofa/core/ObjectFactory.h>
#include "MappedStateObservationManager.inl"
//#include <sofa/helper/accessor.h>

namespace sofa
{

namespace component
{

namespace stochastic
{

using namespace defaulttype;


SOFA_DECL_CLASS(MappedStateObservationManager)

// Register in the Factory
int MappedStateObservationManagerClass = core::RegisterObject("MappedStateObservationManager")
    .add< MappedStateObservationManager<double, Vec3Types, Vec3Types> >(true)
    //.add< MappedStateObservationManager<float, Vec3Types, Vec3Types> >(true)
    ;

template class SOFA_STOCHASTIC_API MappedStateObservationManager<double, Vec3Types, Vec3Types>;
//template class SOFA_STOCHASTIC_API MappedStateObservationManager<float, Vec3Types, Vec3Types>;


} // namespace stochastic
} // namespace component
} // namespace sofa




