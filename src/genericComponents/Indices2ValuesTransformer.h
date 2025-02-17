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
#pragma once

#if !defined(__GNUC__) || (__GNUC__ > 3 || (_GNUC__ == 3 && __GNUC_MINOR__ > 3))
#pragma once
#endif

#include <sofa/core/DataEngine.h>
#include <SofaBaseMechanics/MechanicalObject.h>
#include <sofa/helper/vector.h>

#include "../initOptimusPlugin.h"



namespace sofa
{

namespace component
{

namespace engine
{


template <class DataTypes>
class Indices2ValuesTransformer : public sofa::core::DataEngine
{
public:
    SOFA_CLASS(SOFA_TEMPLATE(Indices2ValuesTransformer,DataTypes),sofa::core::DataEngine);
    typedef typename DataTypes::Coord Coord;
    typedef typename DataTypes::VecCoord VecCoord;
    typedef typename DataTypes::Real Real;
    typedef sofa::defaulttype::Vec<3,Real> Vec3;
    typedef unsigned int Index;

protected:

    Indices2ValuesTransformer();
    ~Indices2ValuesTransformer() {}
public:
    void init() override;
    void reinit() override;
    void doUpdate() override;

    virtual std::string getTemplateName() const override
    {
        return templateName(this);
    }

    static std::string templateName(const Indices2ValuesTransformer<DataTypes>* = NULL)
    {
        return DataTypes::Name();
    }

    //Input
    Data<sofa::helper::vector<Real> > f_inputValues; ///< Already existing values (can be empty) 
    Data<sofa::helper::vector<Real> > f_indices; ///< Indices to map value on 
    Data<sofa::helper::vector<Real> > f_values1, f_values2; ///< Values to map indices on

    //Output
    Data<sofa::helper::vector<Real> > f_outputValues; ///< New map between indices and values

    //Parameter
    Data<Real> p_defaultValue; ///< Default value for indices without any value
    Data<std::string> d_transformation;

};

#if defined(SOFA_EXTERN_TEMPLATE) && !defined(SOFA_COMPONENT_ENGINE_INDICES2VALUESTRANSFORMER_CPP)
#ifndef SOFA_FLOAT
extern template class SOFA_GENERAL_ENGINE_API Indices2ValuesTransformer<sofa::defaulttype::Vec3dTypes>;
#endif //SOFA_FLOAT
#ifndef SOFA_DOUBLE
extern template class SOFA_GENERAL_ENGINE_API Indices2ValuesTransformer<sofa::defaulttype::Vec3fTypes>;
#endif //SOFA_DOUBLE
#endif



} // namespace engine

} // namespace component

} // namespace sofa

